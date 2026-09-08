import sys,os,time,threading,inspect

if len(sys.argv)!=2:
    print("usage: python3 callspy.py <input.py>")
    sys.exit(1)

target=os.path.abspath(sys.argv[1])
root=os.path.dirname(target)
spy=os.path.abspath(__file__)
depth={}

def out(x):
    print(f"[{time.strftime('%H:%M:%S')}] {x}",flush=True)

def allowed(file):
    if not file or file==spy:
        return False
    if file.startswith("<frozen") or file.startswith("<built-in"):
        return False
    if file.startswith("<"):
        return file in ("<string>","<stdin>","<exec>")
    try:
        f=os.path.abspath(file)
        return f==target or f.startswith(root+os.sep)
    except:
        return False

def fmt(v):
    try:
        r=repr(v)
        return r if len(r)<=120 else r[:117]+"..."
    except:
        return "<unrepr>"

def trace(frame,event,arg):
    file=frame.f_code.co_filename

    if not allowed(file):
        return None

    tid=threading.get_ident()
    d=depth.get(tid,0)
    name=frame.f_code.co_name

    if event=="call":
        depth[tid]=d+1
        args=[]

        try:
            a=inspect.getargvalues(frame)
            for n in a.args:
                if n in a.locals:
                    args.append(f"{n}={fmt(a.locals[n])}")
        except:
            pass

        out(f"{'  '*d}CALL {name}({', '.join(args)}) [{os.path.basename(file)}:{frame.f_lineno}]")

    elif event=="return":
        out(f"{'  '*max(0,d-1)}RETURN {name} -> {fmt(arg)}")
        depth[tid]=max(0,d-1)

    elif event=="exception":
        try:
            typ,val,_=arg
            out(f"{'  '*d}EXCEPTION {name}: {typ.__name__}: {val}")
        except:
            pass

    return trace

def thread_trace(frame,event,arg):
    return trace(frame,event,arg)

out(f"START {target}")

old=sys.argv
sys.argv=[target]

try:
    with open(target,"r",encoding="utf-8") as f:
        source=f.read()

    code=compile(source,target,"exec")

    sys.settrace(trace)
    threading.settrace(thread_trace)

    exec(code,{"__name__":"__main__","__file__":target})

except KeyboardInterrupt:
    out("STOP")
except SystemExit as e:
    out(f"EXIT {e}")
except BaseException as e:
    out(f"ERROR {type(e).__name__}: {e}")
finally:
    sys.settrace(None)
    threading.settrace(None)
    sys.argv=old

out("DONE")