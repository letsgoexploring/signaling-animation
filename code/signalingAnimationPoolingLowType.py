from __future__ import division
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.path as path
import subprocess

plt.style.use('classic')

# Parameters for animation
aL=4
cH=0.25
lam=2
eta=2
aH=lam*aL
cL=eta*cH
p = 0.25
aBar = p*aH+(1-p)*aL

eMin = 0
eMax = 10
eStep=0.05

eRange = np.arange(eMin-eStep,eMax+eStep-0.00001,eStep)

#Low type
eLstar = aL/2/cL
uLstar = aL*eLstar-cL*eLstar**2

coeffsL = [-cL,aBar,-uLstar]
eLmax = np.max(np.roots(coeffsL))

costL = cL*eRange**2
uLowL = aL*eRange-costL
uHighL= aBar*eRange-costL

yMinL,yMaxL = -10,15


##########################################


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=6, metadata=dict(artist='Brian C Jenkins'), bitrate=1000)

fig = plt.figure(figsize=(16,9))
ax1 = fig.add_subplot(1, 1, 1)
ax1.grid()
plt.plot(eRange,uHighL,'--',lw=2,color='b')
plt.plot(eRange,uLowL,'--',lw=2,color='r')
line1, = ax1.plot([], [],'k', lw=3)
line2, = ax1.plot([], [],'k', lw=3)
line3, = ax1.plot([], [],'ok', lw=4)
# ax1.set_xlim(eMin, eMax)
# ax1.set_ylim(yMinL,yMaxL)
ax1.set_xlabel('Level of education ($e$)')
ax1.set_ylabel('\n\n')
ax1.legend(['$\\bar{m}e - c_L e^2$','$m_L e - c_L e^2$','$u_L(e)$'],ncol=1,fontsize=20,loc='center left', bbox_to_anchor=(1, 0.5))
ax1.set_title('Type L Worker Utility ($u_L)$',fontsize=20,pad = 10)

# Initialize the shaded rectangle
left = 0
right = 0
bottom = yMinL
top = bottom - yMinL + yMaxL

nverts = 5
verts = np.zeros((nverts, 2))
codes = np.ones(nverts, int) * path.Path.LINETO
codes[0] = path.Path.MOVETO
codes[4] = path.Path.CLOSEPOLY
verts[0,0] = left
verts[0,1] = bottom
verts[1,0] = left
verts[1,1] = top
verts[2,0] = right
verts[2,1] = top
verts[3,0] = right
verts[3,1] = bottom

rectPath = path.Path(verts, codes)
patch = patches.PathPatch(rectPath, facecolor='green', edgecolor='green', alpha=0.5)
ax1.add_patch(patch)

fig.tight_layout()

#############
z,n=10000,0
def run(*args):
    global z,n

    e1 = 0.25

    e = eRange[n]
    util =[]
    for m,x in enumerate(eRange):
        if x<e:
            util.append(uLowL[m])
        else:
            util.append(aBar*e - costL[m])
    if e<e1:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aBar*e - costL[n]])
        xlabels  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = e
        verts[0,0] = left
        verts[1,0] = left
        verts[2,0] = right
        verts[3,0] = right

    elif e1<=e<eLstar:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aBar*e - costL[n]])
        xlabels  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = e
        verts[0,0] = left
        verts[1,0] = left
        verts[2,0] = right
        verts[3,0] = right

    elif eLstar<=e<eLmax:
        ax1.set_xticks([eLstar,eRange[n]])
        ax1.set_yticks([0,uLstar,aBar*e - costL[n]])
        xlabels  = ['$e_L^*$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_L(e_L^*)$','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = e
        verts[0,0] = left
        verts[1,0] = left
        verts[2,0] = right
        verts[3,0] = right

    else:
        ax1.set_xticks([eLstar,eLmax,eRange[n]])
        ax1.set_yticks([0,uLstar,aBar*e - costL[n]])
        xlabels  = ['$e_L^*$','$e_L^{max}$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_L(e_L^*)$','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = eLmax
        verts[0,0] = left
        verts[1,0] = left
        verts[2,0] = right
        verts[3,0] = right
    
    eRange1=eRange[0:n]
    util1 = util[:n]
    eRange2=eRange[n:]
    util2 = util[n:]
    eRange3=eRange[n]
    util3=util[n]
    # fig.savefig("%d.png"%z)
    z+=1
    if n==len(eRange)-1:
        n = len(eRange)-1
    else:
        n+=1
    
    ax1.set_xticklabels(xlabels,fontsize=20)
    ax1.set_yticklabels(ylabels,fontsize=20)
    line1.set_data(eRange1, util1)
    line2.set_data(eRange2, util2)
    line3.set_data(eRange3, util3)

    ax1.set_xlim(eMin, eMax)
    ax1.set_ylim(yMinL,yMaxL)

    return line1,line2,line3

ani = animation.FuncAnimation(fig, run, eRange, blit=False,repeat=False,interval=1)
ani.save('../video/signalingPoolingLow.mp4',writer=writer)
plt.show()


# makegif = 'convert -loop 0 *.png Solow_Animated.gif'
# subprocess.call(makegif,shell=True)

# Convert the mp4 video to ogg format
makeOgg = 'ffmpeg -i ../video/signalingPoolingLow.mp4 -c:v libtheora -c:a libvorbis -q:v 6 -q:a 5 ../video/signalingPoolingLow.ogv'
subprocess.call(makeOgg,shell=True)

