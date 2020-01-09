from .models import Article, Vote
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Article)
def create_first_vote(sender, instance, created, **kwargs):
    if created:
        vote = Vote.objects.create(
            article=instance,
            rating=5
        )
        import inspect
        for frame_record in inspect.stack():
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            vote.ip = ip
            vote.save(update_fields=['ip'])