(function() {
  var onEachFrame;
  if (window.webkitRequestAnimationFrame) {
    onEachFrame = function(cb) {
      var _cb = function() {
        cb();
        webkitRequestAnimationFrame(_cb);
      };
      _cb();
    };
  } else if (window.mozRequestAnimationFrame) {
    onEachFrame = function(cb) {
      var _cb = function() {
        cb();
        mozRequestAnimationFrame(_cb);
      };
      _cb();
    };
  } else {
    onEachFrame = function(cb) {
      setInterval(cb, 1000 / 60);
    };
  }

  window.onEachFrame = onEachFrame;
})();

function Ball(l, t, i) {
  this.l = l;
  this.t = t;
  this.e = "";
  this.i = i;
  this.el = "";
  this.c = 0;
  this.v = [];
  this.u = function() {
    el = document.getElementById("i" + this.i).style;
    el.left = this.l + "px";
    el.top = this.t + "px";
  };
  this.a = function() {
    this.c = Math.floor(Math.random() * 4);
    document.getElementById("bl").innerHTML +=
      "<div class='b b" + this.c + "' id='i" + this.i + "'></div>";
    //this.el=document.getElementById("i" + this.i);
    this.u();
    v = [200 - this.l - 10, 300 - this.t - 10];
    this.v = [
      v[0] / Math.sqrt(v[0] * v[0] + v[1] * v[1]),
      v[1] / Math.sqrt(v[0] * v[0] + v[1] * v[1])
    ];
  };
}

function d(e) {
  k = "which" in e ? e.which : e.keyCode;
  switch (k) {
    case 37:
      lr = -1;
      break;
    case 39:
      lr = 1;
      break;
    case 38:
      if (ss > 10) {
        document.getElementById("s").style.visibility = "visible";
        s = 1;
      }
      break;
    case 40:
      document.getElementById("s").style.visibility = "hidden";
      s = 0;
      break;
  }
}

function u(e) {
  k = "which" in e ? e.which : e.keyCode;
  lr = k == 37 || k == 39 ? 0 : lr;
}

function lo() {
  var wav = new Audio("a.wav");
  wav.play();
  liv -= 1;
  pun -= 5;
  str = 0;
  ml = 1;
  document.getElementById("lv").innerHTML = liv;
  if (liv <= 0) {
    end = 1;
    document.getElementById("end").style.visibility = "visible";

    document.getElementById("ppp").innerHTML = pun + " POINTS";
  }
}

function wi() {
  pun += mul;
  str += 1;

  if (str % 10 == 0) {
    mul *= 2;
    mlI = document.getElementById("ml");
    mlI.innerHTML = "x" + mul;
    mlI.style.visibility = "visible";
    setTimeout(function() {
      document.getElementById("ml").style.visibility = "hidden";
    }, 2000);
  }
}

function l() {
  if (end == 0) {
    //Shield
    if (s == 1) {
      ss -= 0.18;
    } else {
      ss += 0.05;
    }
    if (ss <= 0) {
      s = 0;
      document.getElementById("s").style.visibility = "hidden";
    }
    ss = ss < 0 ? 0 : ss > 100 ? 100 : ss;

    document.getElementById("b2").style.width = ss + "%";
    ////////
    p = document.getElementById("p");
    pd += lr * 3;
    p.style.webkitTransform = "rotate(" + pd + "deg)";
    p.style.mozTransform = "rotate(" + pd + "deg)";
    p.style.msTransform = "rotate(" + pd + "deg)";
    p.style.oTransform = "rotate(" + pd + "deg)";
    p.style.transform = "rotate(" + pd + "deg)";
    // Balls

    if (b.length < 5 && Math.random() * 100 < 2) {
      ////////////////////////////////////
      ll = 0;
      tt = 0;
      r = Math.random();
      ll = Math.floor(Math.random() * 400);
      tt = ll;
      if (r < 0.25) {
        tt = 0;
      } else if (r < 0.5) {
        tt = 600;
      } else if (r < 0.75) {
        ll = 0;
      } else {
        ll = 400;
      }
      t += 1;
      b.push(new Ball(ll, tt, t));
      b[b.length - 1].a();
    }
    ////////

    // Move balls

    for (j = 0; j < b.length; j++) {
      b[j].l += b[j].v[0];
      b[j].t += b[j].v[1];
      b[j].u();
      if (
        (190 - b[j].l) * (190 - b[j].l) + (280 - b[j].t) * (280 - b[j].t) <
        3600
      ) {
        // Collision
        th = -Math.atan2(190 - b[j].l, 280 - b[j].t) / (Math.PI / 180) - pd;
        th = th < 0 ? 360 + th : th;
        for (i = 1; i < 4; i++) {
          if (b[j].c == i && s == 0) {
            if (th >= (i - 1) * 120 && th < 120 * i) {
              wi();
            } else {
              lo();
            }
            document.getElementById("pt").innerHTML = pun;
            document.getElementById("st").innerHTML = "STREAK: " + str;
            if (pun < 0) {
              document.getElementById("pt").style.color = "red";
            } else {
              document.getElementById("pt").style.color = "black";
            }
          }
        }

        if (b[j].c == 0 && s == 0) {
          lo();
          document.getElementById("pt").innerHTML = pun;
          document.getElementById("st").innerHTML = "STREAK: " + str;
          if (pun < 0) {
            document.getElementById("pt").style.color = "red";
          } else {
            document.getElementById("pt").style.color = "black";
          }
        }

        document.getElementById("i" + b[j].i).remove();

        b.splice(j, 1);

        break;
      }
    }

    /////////////
  }
}

t = 0;
b = [];
g = document.getElementById("g");
pd = 0;
lr = 0;
liv = 10;
end = 0;
mul = 1;
str = 0;
pun = 0;
s = 0;
ss = 100;
window.onEachFrame(l);
