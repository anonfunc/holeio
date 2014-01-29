from livereload import Server, shell

server = Server()
server.watch('*')
server.serve()
