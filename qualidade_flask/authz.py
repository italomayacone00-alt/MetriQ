from functools import wraps
from flask import abort, request
from flask_login import current_user


def get_owned_or_404(model, id, owner_field='user_id'):
    """Return the object with given id that belongs to current_user or raise 404.

    Usage: obj = get_owned_or_404(Projeto, id)
    """
    filters = {'id': id, owner_field: current_user.id}
    return model.query.filter_by(**filters).first_or_404()


def require_owner(model, id_arg='id', owner_field='user_id'):
    """Decorator to ensure the current_user owns the requested object.

    It injects the object into the view kwargs using the model name lowercased.
    Example:
      @require_owner(Projeto, 'id')
      def detalhe_projeto(projeto):
          # projeto is provided
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            id_value = kwargs.get(id_arg) or request.view_args.get(id_arg)
            obj = model.query.filter_by(id=id_value, **{owner_field: current_user.id}).first()
            if not obj:
                abort(404)
            # inject
            kwargs[model.__name__.lower()] = obj
            return f(*args, **kwargs)
        return wrapped
    return decorator
