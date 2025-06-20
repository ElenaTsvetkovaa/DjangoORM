
def handle_session(session, autoclose=True):

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                session.begin()
                result = func(*args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
            finally:
                if autoclose:
                    session.close()

        return wrapper
    return decorator



