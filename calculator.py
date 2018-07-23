#!/usr/bin/env python

"""
For your homework this week, you'll be creating a wsgi application of
your own.
You'll create an online calculator that can perform several operations.
You'll need to support:
  * Addition
  * Subtractions
  * Multiplication
  * Division
Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.
Consider the following URL/Response body pairs as tests:
```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```
To submit your homework:
  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""

html_text = """<html>
<head>
<title>WSGI Calulator (lesson04 assignment)</title>
</head>
<body>
<h1>{print_operand_a} {print_operation_sign} {print_operand_b}
= {print_result}</h1>
<hr>
<h3>Examples</h3>
<p><a href="http://localhost:8080/multiply/3/5">multiply/3/5</a></p>
<p><a href="http://localhost:8080/add/23/42">add/23/42</a></p>
<p><a href="http://localhost:8080/subtract/23/42">subtract/23/42</a></p>
<p><a href="http://localhost:8080/divide/22/11">divide/22/11</a></p>
<hr>
</body>
</html>"""


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
      #
        path_info = environ.get('PATH_INFO', None)
        if path_info is None:
            raise NameError
        #
        args = resolve_path(path_info)

        operation_list = ["multiply", "divide", "add", "subtract"]

        if args[0].strip() in operation_list:
            operation = args[0].strip()
        else:
            operation = "failed"
            operation_sign = "f"

        operand_a = int(args[1])
        operand_b = int(args[2])

        if operation == "multiply":
            result = operand_a * operand_b
            operation_sign = "*"
        elif operation == "divide":
            result = operand_a / operand_b
            operation_sign = "/"
        elif operation == "add":
            result = operand_a + operand_b
            operation_sign = "+"
        elif operation == "subtract":
            result = operand_a - operand_b
            operation_sign = "-"
        elif operation == "failed":
            result = "error"
            operation_sign = "f"
        else:
            result = "failed"

        body = html_text.format(
            print_path_info=path_info,
            print_no_entries=len(args),
            print_operation=operation,
            print_operation_sign=operation_sign,
            print_operand_a=operand_a,
            print_operand_b=operand_b,
            print_result=result
        )
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Calculate your url with http://localhost:8080/add/10/10 </h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

def resolve_path(path):
    args = path.strip("/").split("/")
    return args

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
