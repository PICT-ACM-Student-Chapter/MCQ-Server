from django.db import models
from import_export import resources, fields
from .models import Question
import uuid
from django.contrib.postgres.fields import ArrayField
# from import_export.widgets import CharWidget, URLWidget, IntegerWidget


class QuestionResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row["options"] = []
        row["options"].append(row["optionA"])
        row["options"].append(row["optionB"])
        row["options"].append(row["optionC"])
        row["options"].append(row["optionD"])
        del row["optionA"]
        del row["optionB"]
        del row["optionC"]
        del row["optionD"]
        row["options"] = ",".join(row["options"])
        return row
    
    def after_import_row(self, row, row_result, **kwargs):
        # print(row.options)
        # print(row_result.options)
        # row.options = row.options.split(",")
        row["options"] = list(row["options"].split(","))

    class Meta:
        model = Question
        fields = ('id', 'statement', 'options', 'correct_option', 'image_url', "fk_event")


        # statement = fields.Field(column_name='statement', attribute='statement', widget=CharWidget())
        # options = fields.Field(column_name='options', attribute='options', widget=CharWidget())
        # code = fields.Field(column_name='code', attribute='code', widget=CharWidget())
        # image_url = fields.Field(column_name='image_url', attribute='image_url', widget=URLWidget())
        # correct_option = fields.Field(column_name='correct_option', attribute='correct_option', widget=IntegerWidget())