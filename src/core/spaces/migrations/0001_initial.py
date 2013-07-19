# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Space'
        db.create_table(u'spaces_space', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'Write here your description.')),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('logo', self.gf('core.spaces.fields.StdImageField')(max_length=100)),
            ('banner', self.gf('core.spaces.fields.StdImageField')(max_length=100)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mod_debate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mod_proposals', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mod_news', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mod_cal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mod_docs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mod_voting', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'spaces', ['Space'])

        # Adding model 'Entity'
        db.create_table(u'spaces_entity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spaces.Space'], null=True, blank=True)),
        ))
        db.send_create_signal(u'spaces', ['Entity'])

        # Adding model 'Document'
        db.create_table(u'spaces_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spaces.Space'], null=True, blank=True)),
            ('docfile', self.gf('core.spaces.file_validation.ContentTypeRestrictedFileField')(content_types=['application/vnd.openofficeorg.extension', 'application/pdf', 'application/x-pdf', 'application/acrobat', 'applications/vnd.pdf', 'text/pdf', 'text/x-pdf', 'application/doc', 'appl/text', 'application/vnd.msword', 'application/vnd.ms-word', 'application/winword', 'application/word', 'application/x-msw6', 'application/x-msword', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.wordprocessingml.template', 'application/vnd.ms-powerpoint', 'application/mspowerpoint', 'application/ms-powerpoint', 'application/mspowerpnt', 'application/vnd-mspowerpoint', 'application/powerpoint', 'application/x-powerpoint', 'application/x-m', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.presentationml.template', 'application/vnd.ms-excel', 'application/msexcel', 'application/x-msexcel', 'application/x-ms-excel', 'application/vnd.ms-excel', 'application/x-excel', 'application/x-dos_ms_excel', 'application/xls', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.oasis.opendocument.text', 'application/x-vnd.oasis.opendocument.text', 'application/vnd.oasis.opendocument.spreadsheet', 'application/x-vnd.oasis.opendocument.spreadsheet', 'application/vnd.oasis.opendocument.presentation', 'application/x-vnd.oasis.opendocument.presentation', 'text/plain', 'application/txt', 'browser/internal', 'text/anytext', 'widetext/plain', 'widetext/paragraph', 'application/rtf', 'application/x-rtf', 'text/rtf', 'text/richtext', 'application/x-soffice', 'application/vnd.oasis.opendocument.formula', 'application/x-vnd.oasis.opendocument.formula'], max_upload_size=26214400, max_length=100)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'spaces', ['Document'])

        # Adding model 'Event'
        db.create_table(u'spaces_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spaces.Space'], null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event_author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='meeting_author', null=True, to=orm['auth.User'])),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=15, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=15, blank=True)),
        ))
        db.send_create_signal(u'spaces', ['Event'])

        # Adding M2M table for field user on 'Event'
        m2m_table_name = db.shorten_name(u'spaces_event_user')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'spaces.event'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'user_id'])

        # Adding model 'Intent'
        db.create_table(u'spaces_intent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spaces.Space'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('requested_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'spaces', ['Intent'])


    def backwards(self, orm):
        # Deleting model 'Space'
        db.delete_table(u'spaces_space')

        # Deleting model 'Entity'
        db.delete_table(u'spaces_entity')

        # Deleting model 'Document'
        db.delete_table(u'spaces_document')

        # Deleting model 'Event'
        db.delete_table(u'spaces_event')

        # Removing M2M table for field user on 'Event'
        db.delete_table(db.shorten_name(u'spaces_event_user'))

        # Deleting model 'Intent'
        db.delete_table(u'spaces_intent')


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
        u'spaces.document': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Document'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'docfile': ('core.spaces.file_validation.ContentTypeRestrictedFileField', [], {'content_types': "['application/vnd.openofficeorg.extension', 'application/pdf', 'application/x-pdf', 'application/acrobat', 'applications/vnd.pdf', 'text/pdf', 'text/x-pdf', 'application/doc', 'appl/text', 'application/vnd.msword', 'application/vnd.ms-word', 'application/winword', 'application/word', 'application/x-msw6', 'application/x-msword', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.wordprocessingml.template', 'application/vnd.ms-powerpoint', 'application/mspowerpoint', 'application/ms-powerpoint', 'application/mspowerpnt', 'application/vnd-mspowerpoint', 'application/powerpoint', 'application/x-powerpoint', 'application/x-m', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.presentationml.template', 'application/vnd.ms-excel', 'application/msexcel', 'application/x-msexcel', 'application/x-ms-excel', 'application/vnd.ms-excel', 'application/x-excel', 'application/x-dos_ms_excel', 'application/xls', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.oasis.opendocument.text', 'application/x-vnd.oasis.opendocument.text', 'application/vnd.oasis.opendocument.spreadsheet', 'application/x-vnd.oasis.opendocument.spreadsheet', 'application/vnd.oasis.opendocument.presentation', 'application/x-vnd.oasis.opendocument.presentation', 'text/plain', 'application/txt', 'browser/internal', 'text/anytext', 'widetext/plain', 'widetext/paragraph', 'application/rtf', 'application/x-rtf', 'text/rtf', 'text/richtext', 'application/x-soffice', 'application/vnd.oasis.opendocument.formula', 'application/x-vnd.oasis.opendocument.formula']", 'max_upload_size': '26214400', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spaces.Space']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'spaces.entity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Entity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spaces.Space']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'spaces.event': {
            'Meta': {'ordering': "['event_date']", 'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event_author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'meeting_author'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '15', 'blank': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '15', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spaces.Space']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        u'spaces.intent': {
            'Meta': {'object_name': 'Intent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requested_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spaces.Space']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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

    complete_apps = ['spaces']