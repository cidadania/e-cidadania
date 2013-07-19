# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Debate'
        db.create_table(u'debate_debate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spaces.Space'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_mod', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'debate', ['Debate'])

        # Adding model 'Column'
        db.create_table(u'debate_column', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('criteria', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('debate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['debate.Debate'], null=True, blank=True)),
        ))
        db.send_create_signal(u'debate', ['Column'])

        # Adding model 'Row'
        db.create_table(u'debate_row', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('criteria', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('debate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['debate.Debate'], null=True, blank=True)),
        ))
        db.send_create_signal(u'debate', ['Row'])

        # Adding model 'Note'
        db.create_table(u'debate_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('column', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['debate.Column'], null=True, blank=True)),
            ('row', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['debate.Row'], null=True, blank=True)),
            ('debate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['debate.Debate'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=100, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='note_author', null=True, to=orm['auth.User'])),
            ('last_mod_author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='update_author', null=True, to=orm['auth.User'])),
            ('last_mod', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'debate', ['Note'])


    def backwards(self, orm):
        # Deleting model 'Debate'
        db.delete_table(u'debate_debate')

        # Deleting model 'Column'
        db.delete_table(u'debate_column')

        # Deleting model 'Row'
        db.delete_table(u'debate_row')

        # Deleting model 'Note'
        db.delete_table(u'debate_note')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'debate.column': {
            'Meta': {'object_name': 'Column'},
            'criteria': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'debate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['debate.Debate']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'debate.debate': {
            'Meta': {'object_name': 'Debate'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_mod': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spaces.Space']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'debate.note': {
            'Meta': {'object_name': 'Note'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'note_author'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'column': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['debate.Column']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'debate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['debate.Debate']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_mod': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_mod_author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'update_author'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'row': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['debate.Row']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        u'debate.row': {
            'Meta': {'object_name': 'Row'},
            'criteria': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'debate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['debate.Debate']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'spaces.space': {
            'Meta': {'ordering': "['name']", 'object_name': 'Space'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'banner': ('core.spaces.fields.StdImageField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u'Write here your description.'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('core.spaces.fields.StdImageField', [], {'max_length': '100'}),
            'mod_cal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod_debate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod_docs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod_news': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod_proposals': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod_voting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['debate']