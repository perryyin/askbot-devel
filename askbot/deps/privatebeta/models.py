import uuid
import datetime

from django.db import models
from django.template import Context
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from jinja2 import Template

from askbot.skins.loaders import get_template
from askbot.conf import settings as askbot_settings

class InviteRequest(models.Model):
    email = models.EmailField(_('Email address'), unique=True)
    created = models.DateTimeField(_('Created'), default=datetime.datetime.now)
    invited = models.BooleanField(_('Invited'), default=False)
    invitation_code = models.CharField(max_length = 10, blank=True,
                                       unique=True, null=True)
    invited_date = models.DateTimeField(_('Invited Date'),
                                        null=True, blank=True)
    used_invitation = models.BooleanField(_('Used invitation'),
                                          default=False)
    used_invitation_date = models.DateTimeField(_('Used invitation date'),
                                                null=True, blank=True)

    def __unicode__(self):
        return _('Invite for %(email)s') % {'email': self.email}

    def send_invite(self):
        '''Method to send email with invite and update model information
        according to that'''
        self.invited_date = datetime.datetime.now()
        self.invitation_code =  str(uuid.uuid1()).split('-')[0]
        self.invited = True
        data = {
                'code': reverse('privatebeta_activate_invite',
                                args=[self.invitation_code]),
                'domain_name': askbot_settings.APP_URL
               }
        context = Context(data)

        if askbot_settings.PRIVATEBETA_ENABLE_CUSTOM_MESSAGE:
            email_template = Template(askbot_settings.PRIVATEBETA_CUSTOM_MESSAGE)
            email_message = email_template.render(context)
            subject = askbot_settings.PRIVATEBETA_CUSTOM_SUBJECT
        else:
            email_template = get_template('privatebeta/invitation_email.html')
            email_message = email_template.render(context)
            subject = _('Your invitation for s' % data['domain_name'])

        send_mail(subject, email_message,
                'noreply@%s' % data['domain_name'],
                [self.email])
        self.save()

    def invite_used(self):
        self.used_invitation = True
        self.used_invitation_date = datetime.datetime.now()
        self.save()
