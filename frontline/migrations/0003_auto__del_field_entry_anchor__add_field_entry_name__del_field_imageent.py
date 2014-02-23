# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Entry.anchor'
        db.delete_column(u'frontline_entry', 'anchor')

        # Adding field 'Entry.name'
        db.add_column(u'frontline_entry', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'ImageEntry.anchor'
        db.delete_column(u'frontline_imageentry', 'anchor')

        # Adding field 'ImageEntry.name'
        db.add_column(u'frontline_imageentry', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Entry.anchor'
        db.add_column(u'frontline_entry', 'anchor',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Entry.name'
        db.delete_column(u'frontline_entry', 'name')

        # Adding field 'ImageEntry.anchor'
        db.add_column(u'frontline_imageentry', 'anchor',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'ImageEntry.name'
        db.delete_column(u'frontline_imageentry', 'name')


    models = {
        u'frontline.entry': {
            'Meta': {'object_name': 'Entry'},
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'frontline.imageentry': {
            'Meta': {'object_name': 'ImageEntry'},
            'data': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['frontline']