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
eMax = 19
eStep=0.05

eRange = np.arange(eMin-eStep,eMax+eStep-0.00001,eStep)

#High type
eHstar = aL/2/cH
uHstar = aL*eHstar-cH*eHstar**2

coeffsH = [-cH,aBar,-uHstar]
eHmax = np.max(np.roots(coeffsH))

costH = cH*eRange**2
uLowH = aL*eRange-costH
uHighH= aBar*eRange-costH

yMinH,yMaxH = -10,27


##########################################


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=6, metadata=dict(artist='Brian C Jenkins'), bitrate=1000)

fig = plt.figure(figsize=(16,9))
ax1 = fig.add_subplot(1, 1, 1)
ax1.grid()
plt.plot(eRange,uHighH,'--',lw=2,color='b')
plt.plot(eRange,uLowH,'--',lw=2,color='r')
line1, = ax1.plot([], [],'k', lw=3)
line2, = ax1.plot([], [],'k', lw=3)
line3, = ax1.plot([], [],'ok', lw=4)
# ax1.set_xlim(eMin, eMax)
# ax1.set_ylim(yMinH,yMaxH)
ax1.set_xlabel('Level of education ($e$)')
ax1.set_ylabel('\n\n')
ax1.legend(['$\\bar{m}e - c_H e^2$','$m_L e - c_H e^2$','$u_H(e)$'],ncol=1,fontsize=20,loc='center left', bbox_to_anchor=(1, 0.5))
ax1.set_title('Type H Worker Utility ($u_H)$',fontsize=20,pad = 10)

# Initialize the shaded rectangle
left = 0
right = 0
bottom = yMinH
top = bottom - yMinH + yMaxH

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
patch = patches.PathPatch(rectPath, facecolor='red', edgecolor='red', alpha=0.5)
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
            util.append(uLowH[m])
        else:
            util.append(aBar*e - costH[m])
    if e<e1:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aBar*e - costH[n]])
        xlabels  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = e
        verts[0,0] = left
        verts[1,0] = left
        verts[2,0] = right
        verts[3,0] = right


    elif e1<=e<eHstar:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aBar*e - costH[n]])
        xlabels  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = e
        verts[0,0] = left
        verts[1,0] = left
        verts[2,0] = right
        verts[3,0] = right


    elif eHstar<=e<eHmax:
        ax1.set_xticks([eHstar,eRange[n]])
        ax1.set_yticks([0,uHstar,aBar*e - costH[n]])
        xlabels  = ['$e_H^*$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(e_H^*)$','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = e
        verts[0,0] = left
        verts[1,0] = left
        verts[2,0] = right
        verts[3,0] = right


    else:
        ax1.set_xticks([eHstar,eHmax,eRange[n]])
        ax1.set_yticks([0,uHstar,aBar*e - costH[n]])
        xlabels  = ['$e_H^*$','$e_H^{max}$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(e_H^*)$','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        left = 0
        right = eHmax
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
    ax1.set_ylim(yMinH,yMaxH)


    return line1,line2,line3

ani = animation.FuncAnimation(fig, run, eRange, blit=False,repeat=True,interval=1)
ani.save('../video/signalingPoolingHigh.mp4',writer=writer)
plt.show()


# makegif = 'convert -loop 0 *.png Solow_Animated.gif'
# subprocess.call(makegif,shell=True)

# Convert the mp4 video to ogg format
makeOgg = 'ffmpeg -i ../video/signalingPoolingHigh.mp4 -c:v libtheora -c:a libvorbis -q:v 6 -q:a 5 ../video/signalingPoolingHigh.ogv'
subprocess.call(makeOgg,shell=True)
