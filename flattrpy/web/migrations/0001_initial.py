# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('web_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('gravatar', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('web', ['User'])

        # Adding model 'APIToken'
        db.create_table('web_apitoken', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_tokens', null=True, to=orm['web.User'])),
        ))
        db.send_create_signal('web', ['APIToken'])

        # Adding model 'Project'
        db.create_table('web_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('homepage_url', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('thing_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('web', ['Project'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('web_user')

        # Deleting model 'APIToken'
        db.delete_table('web_apitoken')

        # Deleting model 'Project'
        db.delete_table('web_project')


    models = {
        'web.apitoken': {
            'Meta': {'object_name': 'APIToken'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_tokens'", 'null': 'True', 'to': "orm['web.User']"})
        },
        'web.project': {
            'Meta': {'object_name': 'Project'},
            'homepage_url': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'thing_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'web.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'gravatar': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['web']
