class Open:
    def __enter__(self):
        print('open')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('close')

    def __call__(self, *args, **kwargs):
        pass


with Open() as f:
    pass
