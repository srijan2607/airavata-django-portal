#!/usr/bin/env python3
"""
Update Wagtail fixtures for compatibility with Wagtail 4.0+ / 6.x
Changes:
1. wagtailcore.pagerevision -> wagtailcore.revision (already done)
2. Update revision model fields: page -> object_id, content_json -> content
3. Add content_type and base_content_type fields
"""

import json
import glob
import os

def update_revision_entry(entry):
    """Update a revision entry to match Wagtail 4.0+ structure"""
    if entry.get('model') != 'wagtailcore.revision':
        return entry
    
    fields = entry['fields']
    
    # Rename 'page' to 'object_id' and set content_type to page content type
    if 'page' in fields:
        fields['object_id'] = str(fields.pop('page'))
        # Content type 27 is from the original fixture (wagtailapps.base | home page)
        # We'll use a generic page content type
        fields['content_type'] = ['wagtailapps_base', 'homepage']
    
    # Rename 'content_json' to 'content'
    if 'content_json' in fields:
        content_str = fields.pop('content_json')
        # Parse and re-serialize to ensure it's a dict, not a string
        try:
            fields['content'] = json.loads(content_str) if isinstance(content_str, str) else content_str
        except:
            fields['content'] = content_str
    
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
