# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Entry.name'
        db.alter_column(u'frontline_entry', 'name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=250))
        # Adding unique constraint on 'Entry', fields ['name']
        db.create_unique(u'frontline_entry', ['name'])


        # Changing field 'ImageEntry.name'
        db.alter_column(u'frontline_imageentry', 'name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=250))
        # Adding unique constraint on 'ImageEntry', fields ['name']
        db.create_unique(u'frontline_imageentry', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'ImageEntry', fields ['name']
        db.delete_unique(u'frontline_imageentry', ['name'])

        # Removing unique constraint on 'Entry', fields ['name']
        db.delete_unique(u'frontline_entry', ['name'])


        # Changing field 'Entry.name'
        db.alter_column(u'frontline_entry', 'name', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'ImageEntry.name'
        db.alter_column(u'frontline_imageentry', 'name', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

    models = {
        u'frontline.entry': {
            'Meta': {'object_name': 'Entry'},
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'frontline.imageentry': {
            'Meta': {'object_name': 'ImageEntry'},
            'data': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['frontline']