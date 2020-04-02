def rule(event):
    # Capture DeleteBucket, DeleteBucketPolicy, DeleteBucketWebsite
    return event.get('eventName').startswith(
        'DeleteBucket') and not event.get('errorCode')


def dedup(event):
    user_identity = event.get('userIdentity', {})
    if user_identity.get('type') == 'AssumedRole':
        # arn:aws:sts::123456789012:assumed-role/RoleName/<sessionId>
        arn_parts = user_identity.get('arn', '').split('/')
        if arn_parts:
            return '/'.join(arn_parts[:2])
    return user_identity.get('arn')


def title(event):
    user_identity = event.get('userIdentity', {})
    return '{} {} destroyed a bucket'.format(user_identity.get('type'),
                                             dedup(event))
