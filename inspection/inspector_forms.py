from django import forms
from inspection.models import *
from inspection.widgets import ImageSelectWidget
from django.urls import reverse

class InspectionQuestioAnswerForm(forms.models.ModelForm):
    
    FIELDS = {
        TEXT: forms.CharField,
        SHORT_TEXT: forms.CharField,
        SELECT_MULTIPLE: forms.MultipleChoiceField,
        INTEGER: forms.IntegerField,
        FLOAT: forms.FloatField,
        DATE: forms.DateField,
    }

    WIDGETS = {
        TEXT: forms.Textarea,
        SHORT_TEXT: forms.TextInput,
        RADIO: forms.RadioSelect,
        SELECT: forms.Select,
        SELECT_IMAGE: ImageSelectWidget,
        SELECT_MULTIPLE: forms.CheckboxSelectMultiple,
    }

    class Meta:
    	model = Answer
    	fields = ()

    def __init__(self, *args, **kwargs):
        """ Expects a survey object to be passed in initially """
        self.device = kwargs.pop("device")
        self.inspection = kwargs.pop("inspection_name")
        self.user = kwargs.pop("user")
        try:
            self.step = int(kwargs.pop("step"))
        except KeyError:
            self.step = None
        super(InspectionQuestioAnswerForm, self).__init__(*args, **kwargs)
        # self.uuid = uuid.uuid4().hex

        self.categories = self.device.get_question_categories()
        # self.qs_with_no_cat = self.survey.questions.filter(category__isnull=True).order_by("order", "id")

        
        self.steps_count = len(self.categories)
        # will contain prefetched data to avoid multiple db calls

        self.answers = False

        self.add_questions()

        # self._get_preexisting_response()

        # if not self.survey.editable_answers and self.response is not None:
        # for name in self.fields.keys():
        #     self.fields[name].widget.attrs["disabled"] = True

    def add_questions(self):
        if self.step is not None :
            if self.step == len(self.categories):
                qs_for_step = self.device.questions.filter(category__isnull=True).order_by("id")
            else:
                qs_for_step = self.device.questions.filter(category=self.categories[self.step])

            for question in qs_for_step:
                    self.add_question(question)

    def add_question(self, question, data=0):
        """Add a question to the form.

        :param Question question: The question to add.
        :param dict data: The pre-existing values from a post request."""
        kwargs = {"label": question.question_text, "required": False,}
        initial = self.get_question_initial(question, data)
        if initial:
            kwargs["initial"] = initial
        choices = self.get_question_choices(question)
        if choices:
            kwargs["choices"] = choices
        widget = self.get_question_widget(question)
        if widget:
            kwargs["widget"] = widget
        field = self.get_question_field(question, **kwargs)
        field.widget.attrs["category"] = question.category.title if question.category else ""

        if question.answer_type == DATE:
            field.widget.attrs["class"] = "date"
        # logging.debug("Field for %s : %s", question, field.__dict__)
        self.fields["question_%d" % question.pk] = field

    def get_question_widget(self, question):
        """Return the widget we should use for a question.

        :param Question question: The question
        :rtype: django.forms.widget or None"""
        try:
            return self.WIDGETS[question.answer_type]
        except KeyError:
            return None

    @staticmethod
    def get_question_choices(question):
        """Return the choices we should use for a question.

        :param Question question: The question
        :rtype: List of String or None"""
        question_choices = None
        if question.answer_type not in [TEXT, SHORT_TEXT, INTEGER, FLOAT, DATE]:
            question_choices = question.get_choices()
            # add an empty option at the top so that the user has to explicitly
            # select one of the options
            if question.answer_type in [SELECT, SELECT_IMAGE]:
                question_choices = tuple([("", "-------------")]) + question_choices
        return question_choices

    def get_question_field(self, question, **kwargs):
        """Return the field we should use in our form.

        :param Question question: The question
        :param **kwargs: A dict of parameter properly initialized in
            add_question.
        :rtype: django.forms.fields"""
        # logging.debug("Args passed to field %s", kwargs)
        try:
            return self.FIELDS[question.answer_type](**kwargs)
        except KeyError:
            return forms.ChoiceField(**kwargs)

    def current_categories(self):        
        if self.step is not None and self.step < len(self.categories):
            return [self.categories[self.step]]
        return [QuestionCategory(title="No category", description="No cat desc")]

    def has_next_step(self):
        if self.step < self.steps_count - 1:
                return True
        return False

    def next_step_url(self):
        if self.has_next_step():
            context = { 'inspection_name':self.inspection, "device":self.device.name, "pk": self.device.id, "step": self.step + 1}
            return reverse("inspection:inspection-question-answer-form-step", kwargs=context)
    
    def _get_preexisting_answers(self):
        """Recover pre-existing answers in database.

        The user must be logged. A Response containing the Answer must exists.
        Will create an attribute containing the answers retrieved to avoid multiple
        db calls.

        :rtype: dict of Answer or None"""
        if self.answers:
            return self.answers
        try:
            answers = Answer.objects.all().prefetch_related("question")
            self.answers = {answer.question.id: answer for answer in answers.all()}
        except Answer.DoesNotExist:
            self.answers = None

        return self.answers

    def _get_preexisting_answer(self, question):
        """Recover a pre-existing answer in database.

        The user must be logged. A Response containing the Answer must exists.

        :param Question question: The question we want to recover in the
        response.
        :rtype: Answer or None"""
        answers = self._get_preexisting_answers()
        return answers.get(question.id, None)

    def get_question_initial(self, question, data):
        """Get the initial value that we should use in the Form

        :param Question question: The question
        :param dict data: Value from a POST request.
        :rtype: String or None"""
        initial = None
        answer = self._get_preexisting_answer(question)
        if answer:
            # Initialize the field with values from the database if any
            if question.answer_type == SELECT_MULTIPLE:
                initial = []
                if answer.answer_type_text_number == "[]":
                    pass
                elif "[" in answer.answer_type_text_number and "]" in answer.answer_type_text_number:
                    initial = []
                    unformated_choices = answer.answer_type_text_number[1:-1].strip()
                    for unformated_choice in unformated_choices.split(settings.CHOICES_SEPARATOR):
                        choice = unformated_choice.split("'")[1]
                        initial.append(slugify(choice))
                else:
                    # Only one element
                    initial.append(slugify(answer.answer_type_text_number))
            else:
                initial = answer.answer_type_text_number
        if data:
            # Initialize the field field from a POST request, if any.
            # Replace values from the database
            initial = data.get("question_%d" % question.pk)
        return initial


    def save(self, commit=True, *args, **kwargs):
        """ Save the response object """
        # Recover an existing response from the database if any
        #  There is only one response by logged user.
        response = super(InspectionQuestioAnswerForm, self).save(commit=False)
        # response "raw" data as dict (for signal)
        data = {}
        # create an answer object for each question and associate it with this
        # response.
        for field_name, field_value in list(self.data.items()):
            if field_name.startswith("question_"):
                pass
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in
                # the field name in the __init__ method of this form class.
                q_id = int(field_name.split("_")[1])
                question = Question.objects.get(pk=q_id)
                # answer = self._get_preexisting_answer(question)
                # if answer is None:
                answer = Answer(question=question)
                # if question.type == Question.SELECT_IMAGE:
                #     value, img_src = field_value.split(":", 1)
                #     # TODO Handling of SELECT IMAGE
                #     LOGGER.debug("Question.SELECT_IMAGE not implemented, please use : %s and %s", value, img_src)
                if question.answer_type in [TEXT, SHORT_TEXT, INTEGER, FLOAT, SELECT, RADIO, DATE]:
                    answer.answer_type_text_number = field_value
                elif question.answer_type in [SELECT_IMAGE, SELECT_MULTIPLE]:
                    answer.answer_type_image = field_value
                answer.inspector = self.user
                answer.save()
        return response