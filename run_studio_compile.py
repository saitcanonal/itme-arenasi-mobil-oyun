"""Java type/syntax check of studio extension with explicit framework boundary stubs.
Does not validate SQL, Spring wiring or transaction behaviour.
"""
from pathlib import Path
import tempfile,subprocess
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);files=[]
 def put(name,body):
  p=d/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body);files.append(str(p))
 for name in ['org.springframework.stereotype.Service','org.springframework.stereotype.Component','org.springframework.transaction.annotation.Transactional','org.springframework.beans.factory.annotation.Value','org.springframework.web.bind.annotation.RestController','org.springframework.web.bind.annotation.RequestMapping','org.springframework.web.bind.annotation.GetMapping','org.springframework.web.bind.annotation.PostMapping','org.springframework.web.bind.annotation.RequestHeader','org.springframework.web.bind.annotation.RequestBody']:
  pack,cls=name.rsplit('.',1);put(name.replace('.','/')+'.java',f'package {pack};public @interface {cls} {{String value() default "";}}')
 put('org/springframework/jdbc/core/RowMapper.java','package org.springframework.jdbc.core;public interface RowMapper<T>{T mapRow(java.sql.ResultSet r,int n)throws java.sql.SQLException;}')
 put('org/springframework/jdbc/core/JdbcTemplate.java','package org.springframework.jdbc.core;public class JdbcTemplate {public int update(String s,Object... a){throw new UnsupportedOperationException();}public <T>T queryForObject(String s,Class<T> t,Object... a){throw new UnsupportedOperationException();}public <T>T queryForObject(String s,RowMapper<T> t,Object... a){throw new UnsupportedOperationException();}public <T>java.util.List<T> queryForList(String s,Class<T> t,Object... a){throw new UnsupportedOperationException();}}')
 put('com/itmearena/application/AnonymousAuth.java','package com.itmearena.application;public class AnonymousAuth{public record Profile(String playerId){} public Profile current(String bearer){throw new UnsupportedOperationException();}}')
 for name in ['application/StudioService.java','application/NamePolicy.java','application/AuthFailure.java','adapters/http/StudioController.java']:files.append(str(root/'Server/src/main/java/com/itmearena'/name))
 subprocess.run(['java','-m','jdk.compiler/com.sun.tools.javac.Main','-d',str(d/'classes'),*files],check=True)
 print('PASS StudioService / StudioController Java compile against framework boundary stubs. NOT a Spring/PostgreSQL integration test.')
