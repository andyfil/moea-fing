@echo off
IF "%1" == "client" goto client
IF "%1" == "server" goto server

:client
c:\py_cliente\Scripts\activate
goto end
:server
c:\py_env\Scripts\activate
goto end

:end