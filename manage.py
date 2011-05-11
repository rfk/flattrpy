#!/usr/bin/env python
import sys

from django.core.management import execute_manager
import settings

if __name__ == "__main__":
    execute_manager(settings)
