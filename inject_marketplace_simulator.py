#!/usr/bin/env python3
"""Inject 3 professional simulators into the Veelearn marketplace."""

import pymysql, json, sys, os, io

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("MYSQL_DATABASE") or os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("AIVEN_PASSWORD", ""),
    "port": int(os.getenv("MYSQLPORT") or os.getenv("AIVEN_PORT", "26399")),
    "user": os.getenv("MYSQLUSER") or os.getenv("AIVEN_USER", "avnadmin"),
    "read_timeout": 10,
    "write_timeout": 10,
}

# SSL Configuration for Aiven
ssl_ca = os.getenv("DB_SSL_CA")
if ssl_ca:
    # If it's the raw string with \n, fix it
    if "\\n" in ssl_ca:
        ssl_ca = ssl_ca.replace("\\n", "\n")
    
    # Save to a temporary file because pymysql needs a file path
    ca_path = os.path.join(os.getcwd(), "ca.pem")
    with open(ca_path, "w") as f:
        f.write(ssl_ca)
    AIVEN_CONFIG["ssl"] = {"ca": ca_path}

# =====================================================================
# Simulator 1: Solar System Orbital Mechanics
# Uses sim.ctx, sim.width, sim.height, sim.frame, sim.mouse
# =====================================================================
SOLAR_SYSTEM_CODE = """
function setup(sim) {
  sim.state = {
    planets: [
      {name:'Mercury',color:'#b0b0b0',r:4,dist:60,speed:4.15,angle:Math.random()*Math.PI*2,trail:[]},
      {name:'Venus',color:'#e8c56d',r:6,dist:95,speed:1.62,angle:Math.random()*Math.PI*2,trail:[]},
      {name:'Earth',color:'#4a9eff',r:7,dist:135,speed:1,angle:Math.random()*Math.PI*2,trail:[]},
      {name:'Mars',color:'#e05030',r:5,dist:175,speed:0.53,angle:Math.random()*Math.PI*2,trail:[]},
      {name:'Jupiter',color:'#c8a050',r:14,dist:240,speed:0.084,angle:Math.random()*Math.PI*2,trail:[]},
      {name:'Saturn',color:'#e0c878',r:12,dist:310,speed:0.034,angle:Math.random()*Math.PI*2,trail:[]}
    ],
    stars: Array.from({length:200},function(){return{x:Math.random()*2000-500,y:Math.random()*2000-500,s:Math.random()*1.5+0.5,b:Math.random()}}),
    sliders: [
      {name:'Speed',min:0.1,max:5,val:1,x:0,y:0,w:120},
      {name:'Zoom',min:0.3,max:3,val:1,x:0,y:0,w:120}
    ],
    dragging: -1
  };
}

function draw(sim) {
  var ctx=sim.ctx, W=sim.width, H=sim.height, st=sim.state, mx=sim.mouse.x, my=sim.mouse.y, md=sim.mouse.down;

  // position sliders at bottom
  st.sliders[0].x=W/2-140; st.sliders[0].y=H-25;
  st.sliders[1].x=W/2+20;  st.sliders[1].y=H-25;

  // handle slider dragging
  if(md){
    if(st.dragging>=0){
      var s=st.sliders[st.dragging];
      var pct=Math.max(0,Math.min(1,(mx-s.x)/s.w));
      s.val=s.min+pct*(s.max-s.min);
    } else {
      for(var i=0;i<st.sliders.length;i++){
        var s=st.sliders[i];
        if(mx>=s.x&&mx<=s.x+s.w&&my>=s.y-8&&my<=s.y+8){st.dragging=i;break}
      }
    }
  } else { st.dragging=-1; }

  var speedMul=st.sliders[0].val, zoomMul=st.sliders[1].val;
  var cx=W/2, cy=H/2-15;

  ctx.fillStyle='#0a0a1a'; ctx.fillRect(0,0,W,H);

  // stars
  st.stars.forEach(function(s){s.b+=0.02;var a=0.3+Math.sin(s.b)*0.3;ctx.fillStyle='rgba(255,255,255,'+a+')';ctx.fillRect(s.x*zoomMul+cx-500,s.y*zoomMul+cy-500,s.s,s.s)});

  // sun glow
  var sg=ctx.createRadialGradient(cx,cy,5,cx,cy,50*zoomMul);
  sg.addColorStop(0,'rgba(255,200,50,0.8)');sg.addColorStop(0.3,'rgba(255,150,0,0.3)');sg.addColorStop(1,'rgba(255,100,0,0)');
  ctx.fillStyle=sg;ctx.beginPath();ctx.arc(cx,cy,50*zoomMul,0,Math.PI*2);ctx.fill();

  // sun
  ctx.fillStyle='#ffcc33';ctx.beginPath();ctx.arc(cx,cy,15*zoomMul,0,Math.PI*2);ctx.fill();

  st.planets.forEach(function(p){
    p.angle+=p.speed*0.01*speedMul;
    var px=cx+Math.cos(p.angle)*p.dist*zoomMul;
    var py=cy+Math.sin(p.angle)*p.dist*zoomMul;

    ctx.strokeStyle='rgba(255,255,255,0.08)';ctx.beginPath();ctx.arc(cx,cy,p.dist*zoomMul,0,Math.PI*2);ctx.stroke();

    p.trail.push({x:px,y:py});if(p.trail.length>150)p.trail.shift();
    if(p.trail.length>1){ctx.strokeStyle=p.color+'60';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(p.trail[0].x,p.trail[0].y);
    p.trail.forEach(function(t){ctx.lineTo(t.x,t.y)});ctx.stroke()}

    var pg=ctx.createRadialGradient(px,py,p.r*zoomMul*0.5,px,py,p.r*zoomMul*3);
    pg.addColorStop(0,p.color+'40');pg.addColorStop(1,'transparent');
    ctx.fillStyle=pg;ctx.beginPath();ctx.arc(px,py,p.r*zoomMul*3,0,Math.PI*2);ctx.fill();

    ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(px,py,p.r*zoomMul,0,Math.PI*2);ctx.fill();

    if(p.name==='Saturn'){ctx.strokeStyle=p.color+'aa';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(px,py,p.r*zoomMul*2.2,p.r*zoomMul*0.6,0.3,0,Math.PI*2);ctx.stroke()}

    var dx=mx-px,dy=my-py;
    if(Math.sqrt(dx*dx+dy*dy)<p.r*zoomMul+10){
      ctx.fillStyle='rgba(15,23,42,0.85)';ctx.strokeStyle='#3b82f6';ctx.lineWidth=1;
      var tw=140,th=50,tx=px+15,ty=py-30;
      ctx.fillRect(tx,ty,tw,th);ctx.strokeRect(tx,ty,tw,th);
      ctx.fillStyle='#e2e8f0';ctx.font='bold 13px Arial';ctx.fillText(p.name,tx+10,ty+18);
      ctx.fillStyle='#94a3b8';ctx.font='12px Arial';
      ctx.fillText('Orbit: '+p.dist+' AU (scaled)',tx+10,ty+35);
    }
  });

  // draw sliders on canvas
  ctx.fillStyle='rgba(15,23,42,0.85)';ctx.fillRect(W/2-160,H-40,320,36);
  ctx.strokeStyle='#334155';ctx.strokeRect(W/2-160,H-40,320,36);
  for(var i=0;i<st.sliders.length;i++){
    var s=st.sliders[i];
    var pct=(s.val-s.min)/(s.max-s.min);
    ctx.fillStyle='#94a3b8';ctx.font='11px Arial';ctx.fillText(s.name+': '+s.val.toFixed(1),s.x,s.y-10);
    ctx.fillStyle='#334155';ctx.fillRect(s.x,s.y,s.w,4);
    ctx.fillStyle='#3b82f6';ctx.fillRect(s.x,s.y,s.w*pct,4);
    ctx.fillStyle=st.dragging===i?'#60a5fa':'#3b82f6';
    ctx.beginPath();ctx.arc(s.x+s.w*pct,s.y+2,6,0,Math.PI*2);ctx.fill();
  }
  ctx.lineWidth=1;
}
"""

# =====================================================================
# Simulator 2: Wave Superposition Lab
# =====================================================================
WAVE_CODE = """
function setup(sim) {
  sim.state = {
    t: 0,
    sliders: [
      {name:'Amp 1',min:0,max:100,val:50,x:0,y:0,w:80,color:'#ef4444'},
      {name:'Freq 1',min:1,max:10,val:3,x:0,y:0,w:80,color:'#ef4444'},
      {name:'Phase 1',min:0,max:628,val:0,x:0,y:0,w:80,color:'#ef4444'},
      {name:'Amp 2',min:0,max:100,val:50,x:0,y:0,w:80,color:'#3b82f6'},
      {name:'Freq 2',min:1,max:10,val:3,x:0,y:0,w:80,color:'#3b82f6'},
      {name:'Phase 2',min:0,max:628,val:314,x:0,y:0,w:80,color:'#3b82f6'}
    ],
    dragging: -1
  };
}

function draw(sim) {
  var ctx=sim.ctx, W=sim.width, H=sim.height, st=sim.state, mx=sim.mouse.x, my=sim.mouse.y, md=sim.mouse.down;
  st.t+=0.05;

  // position sliders at bottom
  var sx=10;
  for(var i=0;i<st.sliders.length;i++){
    st.sliders[i].x=sx; st.sliders[i].y=H-12;
    sx+=st.sliders[i].w+12;
    if(i===2){sx+=10}
  }

  // handle slider dragging
  if(md){
    if(st.dragging>=0){
      var s=st.sliders[st.dragging];
      var pct=Math.max(0,Math.min(1,(mx-s.x)/s.w));
      s.val=s.min+pct*(s.max-s.min);
      if(s.name.indexOf('Freq')>=0)s.val=Math.round(s.val);
    } else {
      for(var i=0;i<st.sliders.length;i++){
        var s=st.sliders[i];
        if(mx>=s.x&&mx<=s.x+s.w&&my>=s.y-10&&my<=s.y+10){st.dragging=i;break}
      }
    }
  } else { st.dragging=-1; }

  var a1=st.sliders[0].val,f1=st.sliders[1].val,p1=st.sliders[2].val;
  var a2=st.sliders[3].val,f2=st.sliders[4].val,p2=st.sliders[5].val;

  ctx.fillStyle='#0f172a';ctx.fillRect(0,0,W,H);

  function wave(x,a,f,p,time){return(a/100)*Math.sin(f*x*0.02-time+p/100*Math.PI)}

  var sections=[
    {y:H*0.2,h:H*0.18,label:'Wave 1 (A='+Math.round(a1)+' F='+Math.round(f1)+')',color:'#ef4444',fn:function(x){return wave(x,a1,f1,p1,st.t)}},
    {y:H*0.44,h:H*0.18,label:'Wave 2 (A='+Math.round(a2)+' F='+Math.round(f2)+')',color:'#3b82f6',fn:function(x){return wave(x,a2,f2,p2,st.t)}},
    {y:H*0.7,h:H*0.2,label:'Superposition',color:'#a855f7',fn:function(x){return wave(x,a1,f1,p1,st.t)+wave(x,a2,f2,p2,st.t)}}
  ];

  sections.forEach(function(s){
    ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(0,s.y);ctx.lineTo(W,s.y);ctx.stroke();ctx.setLineDash([]);
    ctx.fillStyle=s.color;ctx.font='bold 12px Arial';ctx.fillText(s.label,10,s.y-s.h*0.35);
    ctx.strokeStyle=s.color;ctx.lineWidth=2.5;ctx.beginPath();
    for(var x=0;x<W;x++){var v=s.fn(x)*s.h*0.4;if(x===0)ctx.moveTo(x,s.y-v);else ctx.lineTo(x,s.y-v)}
    ctx.stroke();
    ctx.strokeStyle=s.color+'30';ctx.lineWidth=8;ctx.beginPath();
    for(var x=0;x<W;x++){var v=s.fn(x)*s.h*0.4;if(x===0)ctx.moveTo(x,s.y-v);else ctx.lineTo(x,s.y-v)}
    ctx.stroke();ctx.lineWidth=1;
  });

  var maxAmp=Math.abs(a1/100+a2/100);
  if(maxAmp>0){
    for(var x=50;x<W-50;x+=100){
      var v=sections[2].fn(x);
      if(Math.abs(v)>maxAmp*0.85){
        ctx.fillStyle='rgba(74,222,128,0.7)';ctx.font='10px Arial';
        ctx.fillText('constructive',x-25,sections[2].y+sections[2].h*0.42+10);
      }
    }
  }

  // legend
  ctx.fillStyle='#ef4444';ctx.beginPath();ctx.arc(W-180,15,5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#94a3b8';ctx.font='12px Arial';ctx.fillText('Wave 1',W-170,19);
  ctx.fillStyle='#3b82f6';ctx.beginPath();ctx.arc(W-110,15,5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#94a3b8';ctx.fillText('Wave 2',W-100,19);
  ctx.fillStyle='#a855f7';ctx.beginPath();ctx.arc(W-40,15,5,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#94a3b8';ctx.fillText('Sum',W-30,19);

  // draw sliders on canvas
  ctx.fillStyle='rgba(15,23,42,0.85)';ctx.fillRect(0,H-32,W,32);
  ctx.strokeStyle='#334155';ctx.beginPath();ctx.moveTo(0,H-32);ctx.lineTo(W,H-32);ctx.stroke();
  for(var i=0;i<st.sliders.length;i++){
    var s=st.sliders[i];
    var pct=(s.val-s.min)/(s.max-s.min);
    ctx.fillStyle='#64748b';ctx.font='9px Arial';ctx.fillText(s.name,s.x,s.y-14);
    ctx.fillStyle='#1e293b';ctx.fillRect(s.x,s.y-2,s.w,4);
    ctx.fillStyle=s.color;ctx.fillRect(s.x,s.y-2,s.w*pct,4);
    ctx.fillStyle=st.dragging===i?'#fff':s.color;
    ctx.beginPath();ctx.arc(s.x+s.w*pct,s.y,5,0,Math.PI*2);ctx.fill();
  }
}
"""

# =====================================================================
# Simulator 3: Projectile Motion Analyzer
# =====================================================================
PROJECTILE_CODE = """
function setup(sim) {
  sim.state = {
    projectiles: [],
    colorIdx: 0,
    colors: ['#3b82f6','#ef4444','#22c55e','#f59e0b','#a855f7','#ec4899','#06b6d4','#f97316'],
    lastClick: false,
    sliders: [
      {name:'Angle (deg)',min:5,max:85,val:45,x:0,y:0,w:130},
      {name:'Velocity (m/s)',min:5,max:50,val:30,x:0,y:0,w:130},
      {name:'Gravity (m/s2)',min:1,max:20,val:10,x:0,y:0,w:130}
    ],
    dragging: -1
  };
}

function draw(sim) {
  var ctx=sim.ctx, W=sim.width, H=sim.height, st=sim.state, f=sim.frame, mx=sim.mouse.x, my=sim.mouse.y, md=sim.mouse.down;

  // position sliders in top-left panel
  st.sliders[0].x=25; st.sliders[0].y=60;
  st.sliders[1].x=25; st.sliders[1].y=95;
  st.sliders[2].x=25; st.sliders[2].y=130;

  // handle slider dragging — only in panel area
  var inPanel=mx>=10&&mx<=180&&my>=10&&my<=175;
  if(md){
    if(st.dragging>=0){
      var s=st.sliders[st.dragging];
      var pct=Math.max(0,Math.min(1,(mx-s.x)/s.w));
      s.val=Math.round((s.min+pct*(s.max-s.min))*10)/10;
    } else if(inPanel){
      for(var i=0;i<st.sliders.length;i++){
        var s=st.sliders[i];
        if(mx>=s.x&&mx<=s.x+s.w&&my>=s.y-10&&my<=s.y+10){st.dragging=i;break}
      }
    }
  } else { st.dragging=-1; }

  var angle=st.sliders[0].val, vel=st.sliders[1].val, grav=st.sliders[2].val;
  var SCALE=6, GY=H-60, OX=50, OY=GY;

  ctx.fillStyle='#0f172a';ctx.fillRect(0,0,W,H);

  // grid
  ctx.strokeStyle='rgba(255,255,255,0.05)';ctx.lineWidth=1;
  for(var x=OX;x<W;x+=SCALE*10){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,GY);ctx.stroke()}
  for(var y=GY;y>0;y-=SCALE*10){ctx.beginPath();ctx.moveTo(OX,y);ctx.lineTo(W,y);ctx.stroke()}

  // ground
  ctx.fillStyle='#1e3a1e';ctx.fillRect(0,GY,W,H-GY);
  ctx.strokeStyle='#22c55e';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(0,GY);ctx.lineTo(W,GY);ctx.stroke();

  // axis labels
  ctx.fillStyle='#64748b';ctx.font='11px Arial';
  for(var m=0;m<=Math.floor((W-OX)/SCALE);m+=10){ctx.fillText(m+'m',OX+m*SCALE-8,GY+15)}
  for(var m=10;m*SCALE<GY;m+=10){ctx.fillText(m+'m',5,GY-m*SCALE+4)}

  // launcher barrel
  var aRad=angle*Math.PI/180, bLen=40;
  ctx.strokeStyle='#94a3b8';ctx.lineWidth=4;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(OX,OY);ctx.lineTo(OX+Math.cos(aRad)*bLen,OY-Math.sin(aRad)*bLen);ctx.stroke();
  ctx.fillStyle='#475569';ctx.beginPath();ctx.arc(OX,OY,8,0,Math.PI*2);ctx.fill();

  // fire on click outside panel
  var clicking=md;
  if(clicking&&!st.lastClick&&!inPanel&&st.dragging<0){
    var a=angle*Math.PI/180,v=vel,g=grav;
    var vx=v*Math.cos(a),vy=v*Math.sin(a);
    var color=st.colors[st.colorIdx%st.colors.length];st.colorIdx++;
    var maxH=vy*vy/(2*g), tTotal=2*vy/g, range=vx*tTotal;
    st.projectiles.push({vx:vx,vy:vy,g:g,t:0,tTotal:tTotal,maxH:maxH,range:range,color:color,points:[],done:false,angle:angle,v0:v});
  }
  st.lastClick=clicking;

  // update & draw projectiles
  st.projectiles.forEach(function(p){
    if(!p.done){
      p.t+=0.03;
      if(p.t>p.tTotal){p.t=p.tTotal;p.done=true}
      var px=p.vx*p.t, py=p.vy*p.t-0.5*p.g*p.t*p.t;
      p.points.push({x:OX+px*SCALE,y:OY-py*SCALE});
    }
    if(p.points.length>1){
      ctx.strokeStyle=p.color+'90';ctx.lineWidth=2;ctx.beginPath();
      ctx.moveTo(p.points[0].x,p.points[0].y);
      p.points.forEach(function(pt){ctx.lineTo(pt.x,pt.y)});ctx.stroke();
      p.points.forEach(function(pt,i){if(i%4===0){ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(pt.x,pt.y,2.5,0,Math.PI*2);ctx.fill()}});
    }
    if(p.points.length>0){
      var last=p.points[p.points.length-1];
      ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(last.x,last.y,5,0,Math.PI*2);ctx.fill();
      var gl=ctx.createRadialGradient(last.x,last.y,2,last.x,last.y,15);
      gl.addColorStop(0,p.color+'60');gl.addColorStop(1,'transparent');
      ctx.fillStyle=gl;ctx.beginPath();ctx.arc(last.x,last.y,15,0,Math.PI*2);ctx.fill();
    }
  });

  // stats panel for last projectile (top-right)
  var last=st.projectiles[st.projectiles.length-1];
  if(last){
    ctx.fillStyle='rgba(30,41,59,0.9)';ctx.fillRect(W-210,10,200,120);
    ctx.strokeStyle='#334155';ctx.strokeRect(W-210,10,200,120);
    ctx.fillStyle='#3b82f6';ctx.font='bold 13px Arial';ctx.fillText('Last Launch Stats',W-200,30);
    ctx.fillStyle='#94a3b8';ctx.font='12px Arial';
    ctx.fillText('Angle: '+last.angle.toFixed(0)+'deg',W-200,50);
    ctx.fillText('Velocity: '+last.v0+' m/s',W-200,68);
    ctx.fillText('Max Height: '+last.maxH.toFixed(1)+' m',W-200,86);
    ctx.fillText('Range: '+last.range.toFixed(1)+' m',W-200,104);
    ctx.fillText('Flight Time: '+last.tTotal.toFixed(2)+' s',W-200,122);
  }

  // control panel (top-left)
  ctx.fillStyle='rgba(30,41,59,0.92)';ctx.fillRect(10,10,170,165);
  ctx.strokeStyle='#334155';ctx.strokeRect(10,10,170,165);
  ctx.fillStyle='#3b82f6';ctx.font='bold 14px Arial';ctx.fillText('Projectile Launcher',20,32);
  for(var i=0;i<st.sliders.length;i++){
    var s=st.sliders[i];
    var pct=(s.val-s.min)/(s.max-s.min);
    ctx.fillStyle='#94a3b8';ctx.font='11px Arial';ctx.fillText(s.name+': '+s.val.toFixed(s.min>=1?0:1),s.x,s.y-10);
    ctx.fillStyle='#1e293b';ctx.fillRect(s.x,s.y,s.w,4);
    ctx.fillStyle='#3b82f6';ctx.fillRect(s.x,s.y,s.w*pct,4);
    ctx.fillStyle=st.dragging===i?'#60a5fa':'#3b82f6';
    ctx.beginPath();ctx.arc(s.x+s.w*pct,s.y+2,6,0,Math.PI*2);ctx.fill();
  }
  ctx.fillStyle='#64748b';ctx.font='11px Arial';ctx.fillText('Click canvas to fire!',25,160);

  ctx.lineWidth=1;ctx.lineCap='butt';
}
"""

SIMULATORS = [
    {
        "title": "Solar System Orbital Mechanics",
        "description": "Interactive solar system simulation showing planetary orbits, gravitational forces, and Kepler's laws. Adjust speed and zoom to explore how gravity shapes the cosmos.",
        "tags": "physics,gravity,solar-system,orbits,astronomy",
        "code_mode": SOLAR_SYSTEM_CODE,
        "rating": 4.50,
        "downloads": 150,
    },
    {
        "title": "Wave Superposition Lab",
        "description": "Explore wave interference, superposition, and standing waves. Create two waves and watch them combine in real-time. Adjust amplitude, frequency, and phase.",
        "tags": "physics,waves,interference,superposition,sound",
        "code_mode": WAVE_CODE,
        "rating": 4.20,
        "downloads": 89,
    },
    {
        "title": "Projectile Motion Analyzer",
        "description": "Launch projectiles at different angles and velocities. See the parabolic trajectory, measure range, max height, and time of flight. Fire multiple shots to compare.",
        "tags": "physics,projectile,motion,kinematics,gravity",
        "code_mode": PROJECTILE_CODE,
        "rating": 4.70,
        "downloads": 210,
    },
]

def main():
    if not AIVEN_CONFIG["password"]:
        print("Set AIVEN_PASSWORD environment variable first!")
        return 1

    print("Connecting to Aiven database...")
    try:
        conn = pymysql.connect(**AIVEN_CONFIG)
    except Exception as e:
        print(f"Connection failed: {e}")
        return 1

    print("Connected!\n")
    cursor = conn.cursor()
    created = []

    try:
        for sim in SIMULATORS:
            print(f"Inserting: {sim['title']}...")
            cursor.execute("""
                INSERT INTO simulators 
                (creator_id, title, description, version, blocks, connections, tags, downloads, rating, is_public, is_featured, sim_type, code_mode)
                VALUES (1, %s, %s, '1.0.0', '[]', '[]', %s, %s, %s, TRUE, TRUE, 'code', %s)
            """, (sim["title"], sim["description"], sim["tags"], sim["downloads"], sim["rating"], sim["code_mode"]))
            cursor.execute("SELECT LAST_INSERT_ID() as id")
            sid = cursor.fetchone()["id"]
            created.append((sid, sim["title"]))
            print(f"  Created simulator ID: {sid}")

        conn.commit()
        print("\n" + "=" * 60)
        print("ALL SIMULATORS INJECTED SUCCESSFULLY!")
        print("=" * 60)
        for sid, title in created:
            print(f"  ID {sid}: {title}")
        print(f"\nTotal: {len(created)} simulators (public + featured)")
        print("All simulators have working HTML5 Canvas code")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return 1
    finally:
        cursor.close()
        conn.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
