import code


class Console(code.InteractiveConsole):
    '''
    Interactive console providing a sandboxed namespace for executing code
    examples.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        namespace=None,
        ):
        namespace = namespace or {}
        namespace['__builtins__'] = __builtins__.copy()
        namespace['__name__'] = '__main__'
        namespace['__package__'] = None
        code.InteractiveConsole.__init__(self,
            locals=namespace,
            filename='<stdin>',
            )
        self.client = client

    ### PUBLIC METHODS ###

    def showsyntaxerror(self, filename=None):
        r'''Proxies Python's InteractiveConsole.showsyntaxerror().
        '''
        code.InteractiveConsole.showsyntaxerror(self, filename=filename)
        self.client.register_error()

    def showtraceback(self):
        r'''Proxies Python's InteractiveConsole.showtraceback().
        '''
        code.InteractiveConsole.showtraceback(self)
        self.client.register_error()

    def unregister_error(self):
        r'''Unregisters the last error registered in the current document
        handler.

        This occurs when the interpreting code block permits errors to appear.
        '''
        if self.client:
            self.client.unregister_error()

    ### PUBLIC PROPERTIES ###

    @property
    def errored(self):
        r'''Is true if the last line executed by the console errored.
        '''
        if self.client:
            return self.client.errored
        return False
