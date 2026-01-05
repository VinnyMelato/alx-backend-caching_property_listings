import logging
from django.core.cache import cache
from django.db import models
from .models import Property
import django_redis

logger = logging.getLogger('properties')

def get_all_properties():
    """Low-level cache for Property queryset (1 hour)."""
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values())  # Serialize to list of dicts for cache
        cache.set('all_properties', properties, 3600)  # 1 hour
        logger.info("Queryset fetched from DB and cached.")
    else:
        logger.info("Queryset retrieved from cache.")
    return [Property(**p) for p in properties]  # Reconstruct objects if needed; here returning list of dicts for view

def get_redis_cache_metrics():
    """Retrieve and analyze Redis cache hit/miss metrics."""
    from django_redis import get_redis_connection
    redis_conn = get_redis_connection('default')
    info = redis_conn.info()
    hits = int(info.get('keyspace_hits', 0))
    misses = int(info.get('keyspace_misses', 0))
    total = hits + misses
    hit_ratio = (hits / total * 100) if total > 0 else 0
    metrics = {
        'hits': hits,
        'misses': misses,
        'hit_ratio': round(hit_ratio, 2),
    }
    logger.info(f"Cache metrics: {metrics}")
    return metrics