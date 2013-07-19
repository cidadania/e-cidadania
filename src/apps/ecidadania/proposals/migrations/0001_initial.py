# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'proposals_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_pk', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'proposals', ['Category'])

        # Adding model 'ProposalSet'
        db.create_table(u'proposals_proposalset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spaces.Space'], null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('debate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['debate.Debate'], null=True, blank=True)),
        ))
        db.send_create_signal(u'proposals', ['ProposalSet'])

        # Adding model 'Proposal'
        db.create_table(u'proposals_proposal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_pk', self.gf('django.db.models.fields.TextField')(null=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('proposalset', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proposal_in', null=True, to=orm['proposals.ProposalSet'])),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('space', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spaces.Space'], null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proposal_authors', null=True, to=orm['auth.User'])),
            ('tags', self.gf('apps.thirdparty.tagging.fields.TagField')(max_length=255, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=15, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=15, blank=True)),
            ('closed', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('closed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proposal_closed_by', null=True, to=orm['auth.User'])),
            ('close_reason', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('merged', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('anon_allowed', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('refurbished', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('budget', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('mod_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'proposals', ['Proposal'])

        # Adding M2M table for field merged_proposals on 'Proposal'
        m2m_table_name = db.shorten_name(u'proposals_proposal_merged_proposals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_proposal', models.ForeignKey(orm[u'proposals.proposal'], null=False)),
            ('to_proposal', models.ForeignKey(orm[u'proposals.proposal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_proposal_id', 'to_proposal_id'])

        # Adding M2M table for field support_votes on 'Proposal'
        m2m_table_name = db.shorten_name(u'proposals_proposal_support_votes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proposal', models.ForeignKey(orm[u'proposals.proposal'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['proposal_id', 'user_id'])

        # Adding M2M table for field votes on 'Proposal'
        m2m_table_name = db.shorten_name(u'proposals_proposal_votes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proposal', models.ForeignKey(orm[u'proposals.proposal'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['proposal_id', 'user_id'])

        # Adding model 'ProposalField'
        db.create_table(u'proposals_proposalfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proposalset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['proposals.ProposalSet'])),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'proposals', ['ProposalField'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'proposals_category')

        # Deleting model 'ProposalSet'
        db.delete_table(u'proposals_proposalset')

        # Deleting model 'Proposal'
        db.delete_table(u'proposals_proposal')

        # Removing M2M table for field merged_proposals on 'Proposal'
        db.delete_table(db.shorten_name(u'proposals_proposal_merged_proposals'))

        # Removing M2M table for field support_votes on 'Proposal'
        db.delete_table(db.shorten_name(u'proposals_proposal_support_votes'))

        # Removing M2M table for field votes on 'Proposal'
        db.delete_table(db.shorten_name(u'proposals_proposal_votes'))

        # Deleting model 'ProposalField'
        db.delete_table(u'proposals_proposalfield')


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
        u'proposals.category': {
            'Meta': {'object_name': 'Category'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'proposals.proposal': {
            'Meta': {'object_name': 'Proposal'},
            'anon_allowed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proposal_authors'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'close_reason': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proposal_closed_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '15', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '15', 'blank': 'True'}),
            'merged': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'merged_proposals': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'merged_proposals_rel_+'", 'null': 'True', 'to': u"orm['proposals.Proposal']"}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'proposalset': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proposal_in'", 'null': 'True', 'to': u"orm['proposals.ProposalSet']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'refurbished': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spaces.Space']", 'null': 'True', 'blank': 'True'}),
            'support_votes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'support_votes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'tags': ('apps.thirdparty.tagging.fields.TagField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'votes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'voting_votes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'proposals.proposalfield': {
            'Meta': {'object_name': 'ProposalField'},
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposalset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['proposals.ProposalSet']"})
        },
        u'proposals.proposalset': {
            'Meta': {'object_name': 'ProposalSet'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'debate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['debate.Debate']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spaces.Space']", 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['proposals']