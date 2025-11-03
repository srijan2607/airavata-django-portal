#!/usr/bin/env python3
"""
Update Wagtail fixtures for compatibility with Wagtail 4.0+ / 6.x
Changes:
1. wagtailcore.pagerevision -> wagtailcore.revision (already done)
2. Update revision model fields to match Wagtail 4.0+ schema
"""

import json
import glob
import os

# Fields that exist in Wagtail 4.0+ Revision model
VALID_REVISION_FIELDS = {
    'content_type', 'object_id', 'created_at', 'user', 'content', 
    'approved_go_live_at', 'base_content_type'
}

# Old fields that need to be removed
DEPRECATED_FIELDS = {
    'page', 'content_json', 'submitted_for_moderation'
}

def update_revision_entry(entry):
    """Update a revision entry to match Wagtail 4.0+ structure"""
    if entry.get('model') != 'wagtailcore.revision':
        return entry
    
    fields = entry['fields'].copy()
    new_fields = {}
    
    # Migrate page -> object_id
    if 'page' in fields:
        new_fields['object_id'] = str(fields['page'])
        # Set content_type - wagtailapps_base.homepage
        new_fields['content_type'] = ['wagtailapps_base', 'homepage']
    
    # Migrate content_json -> content
    if 'content_json' in fields:
        content_str = fields['content_json']
        try:
            new_fields['content'] = json.loads(content_str) if isinstance(content_str, str) else content_str
        except:
            new_fields['content'] = content_str
    
    # Keep only valid fields
    for field, value in fields.items():
        if field not in DEPRECATED_FIELDS and field not in new_fields:
            if field in VALID_REVISION_FIELDS or field not in ('page', 'content_json', 'submitted_for_moderation'):
                new_fields[field] = value
    
    entry['fields'] = new_fields
    return entry

def update_fixture_file(filepath):
    """Update a single fixture file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Update all revision entries
        updated_data = [update_revision_entry(entry) for entry in data]
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(updated_data, f, indent=2)
        
        print(f"✓ Updated {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")
        return False

def main():
    # Find all fixture files
    fixture_files = glob.glob('/app/**/fixtures/**/*.json', recursive=True)
    
    updated = 0
    for filepath in fixture_files:
        if update_fixture_file(filepath):
            updated += 1
    
    print(f"\nUpdated {updated} out of {len(fixture_files)} fixture files")

if __name__ == '__main__':
    main()
