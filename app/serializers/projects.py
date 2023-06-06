def projectSerializer(project):
    return {
            'id': str(project['_id']),        
            'name': project['name'],
            'description': project['description'],
            'created_at': project['created_at'],
            'updated_at': project['updated_at'],
            'created_by': project['created_by']
    }

def projectsSerializer(projects):
    return list(map(lambda project: projectSerializer(project), projects))
