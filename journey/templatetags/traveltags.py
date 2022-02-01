from django import template

register = template.Library()


# simple helper to make building the url easier
@register.simple_tag(takes_context=True)
def blog_url(context, param, value):
    request = context['request']
    full_path_parts = request.get_full_path().split('?')
    if len(full_path_parts) == 1:
        return '?' + param + '=' + str(value)
    else:
        query_string_parts = list()
        params = full_path_parts[1].split('&')
        found_param = False
        for i in params:
            param_parts = i.split('=')
            if param_parts[0] == param:
                found_param = True
                if param == "sort":
                    if value == param_parts[1]:
                        if param_parts[1][0] == '-':
                            query_string_parts.append(param + '=' + str(value))
                        else:
                            query_string_parts.append(param + '=-' + str(value))
                    else:
                        query_string_parts.append(param + '=' + str(value))
                else:
                    query_string_parts.append(param + '=' + str(value))
            else:
                query_string_parts.append(i)
        if not found_param:
            query_string_parts.append(param + '=' + str(value))
        return '?' + "&".join(query_string_parts)

@register.simple_tag
def activesort(sort, field):
    if ( field=='date' and (sort=='date' or sort=='-date' or not sort) )   \
       or (field=='comment_count' and (sort=='comment_count' or sort=='-comment_count') ) \
       or ( field=='latest_comment' and (sort=='latest_comment' or sort=='-latest_comment') ):
        return 'primary active'
    return 'secondary'