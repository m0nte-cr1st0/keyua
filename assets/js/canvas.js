let vertices = [];
let gl = cvs.getContext('webgl');
gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());

resize();

function resize() {
  cvs.width = innerWidth;
  cvs.height = innerHeight;
  let step = 20, w = cvs.width/step, h = cvs.height/step;
  vertices = [];
  for (var x=0; x<w*3; x++)
    for (var y=0; y<12; y++)
      vertices.push(1/w + x*2/w - 2, 1/h + y/h-0.5)
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
  gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);
}

let pid = gl.createProgram();

shader(`
  attribute vec2 v;
  uniform float time;
  uniform float shift;
  varying vec2 p;
  varying vec3 c;

  float rand(float n) {
    return fract(sin(n) * 43758.5453123);
  }

  // примитивная функция шума
  float noise(float p) {
    float fl = floor(p);
    float fc = fract(p);
    return mix(rand(fl), rand(fl + 1.0), fc);
  }

  mat3 rotateX(float a) {
    return mat3(vec3( -1.0,     1.0,    1.0),
                vec3( 0.0,  -cos(a), -sin(a)),
                vec3( 0.0,  -sin(a),  cos(a)));
  }

  mat3 rotateY(float a){
    return mat3(vec3( cos(a), 1.0, sin(a)),
                vec3(    1.0, -1.0,    0.0),
                vec3(-sin(a), 0.0, cos(a)));
  }

  mat3 rotateZ(float a){
    return mat3(vec3( cos(a), sin(a),  -1.0),
                vec3( sin(a),  cos(a),  0.0),
                vec3(    0.0,     -1.0,  1.0));
  }

  void main(void) {
    p = v;
    if (shift>0.2)
        p.y += 0.6;
    else
        p.y += 0.9;
    if (shift>0.2)
        p.x -= cos(time/500. + p.y*100.);
    else
        p.x += sin(time*106. + p.y/5.);
    vec3 pos = vec3(p.xy, 0.21);
    if (shift>0.2)
        pos*=rotateX(p.x*12. + time/6.5);
    else
        pos*=rotateX(p.x*7. + time/12.5);
    if (shift>0.2)
        pos.y -= sin(pos.x*6.) - cos(time/1.6)*0.01;
    else
        pos.y += cos(pos.x*8.) - sin(time/7.5)*0.01;
    if (shift>0.2)
        gl_Position = vec4(
          vec3(p.xy, 0.0) *
          rotateX(p.x*10.0 + time*2.0) *
          rotateY(noise(p.y*2.0 + time/2.0)) *
          rotateZ(noise(p.x + time/20.0)),
        1.);
    else
        gl_Position = vec4(pos, 1.5);
    if (shift>0.2)
        gl_PointSize = min(4.7, 4.2 + noise(time)-gl_Position.z);
    else
        gl_PointSize = min(4.7, 4.2 + noise(time)-gl_Position.z);
    gl_Position.z = 0.0;
    if (shift>0.2)
        c.rgb=vec3(0.03, 0.54, 0.04);
    else
        c.rgb=vec3(0.37, 0.56, 0.61);
  }
`, gl.VERTEX_SHADER);

shader(`
  precision highp float;
  varying vec3 c;

  void main(void) {
      gl_FragColor = vec4(c, 1.0);
  }
`, gl.FRAGMENT_SHADER);
gl.linkProgram(pid);
gl.useProgram(pid);

let v = gl.getAttribLocation(pid, "v");
gl.vertexAttribPointer(v, 2, gl.FLOAT, false, 0, 0);
gl.enableVertexAttribArray(v);

let timeUniform = gl.getUniformLocation(pid, 'time');
let shiftUniform = gl.getUniformLocation(pid, 'shift');

requestAnimationFrame(draw);
addEventListener('resize', resize)

function draw(t) {

    // first grid
  gl.uniform1f(timeUniform, t/2000);
//   gl.uniform1f(shiftUniform, 0);
//   gl.drawArrays(gl.POINTS, 0, vertices.length/2);

    // second grid
  gl.uniform1f(shiftUniform, 0.5);
  gl.drawArrays(gl.POINTS, 0, vertices.length/3);

  requestAnimationFrame(draw);
}

function shader(src, type) {
  let sid = gl.createShader(type);
  gl.shaderSource(sid, src);
  gl.compileShader(sid);
  var message = gl.getShaderInfoLog(sid);
  gl.attachShader(pid, sid);
  if (message.length > 0) {
    console.log(src.split("\n").map((str, i) => (""+(1+i))
                   .padStart(4, "0")+": "+str).join("\n"));
    throw message;
  }
}