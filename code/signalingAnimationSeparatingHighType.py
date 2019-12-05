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
eMax = aH/cH
eStep=0.05

eRange = np.arange(eMin-eStep,eMax+eStep,eStep)

#High type
eHstar = aL/2/cH
uHstar = aL*eHstar-cH*eHstar**2

coeffsH = [-cH,aH,-uHstar]
eHmax = np.max(np.roots(coeffsH))

costH = cH*eRange**2
uLowH = aL*eRange-costH
uHighH= aH*eRange-costH

yMinH,yMaxH = -10,65


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
ax1.set_xlim(eMin, eMax)
ax1.set_ylim(yMinH,yMaxH)
ax1.set_xlabel('Level of education ($e$)')
ax1.set_ylabel('\n\n')
ax1.legend(['$m_He - k_H e^2$','$m_L e - k_L e^2$','$u_L(e)$'],ncol=1,fontsize=20,loc='center left', bbox_to_anchor=(1, 0.5))
ax1.set_title('Type H Worker Utility ($u_H)$',fontsize=20,pad = 10)

# Initialize the shaded rectangle
left = 0
right = 0

bottomH = yMinH
topH = bottomH - yMinH + yMaxH

nverts = 5

vertsH = np.zeros((nverts, 2))
codesH = np.ones(nverts, int) * path.Path.LINETO
codesH[0] = path.Path.MOVETO
codesH[4] = path.Path.CLOSEPOLY
vertsH[0,0] = left
vertsH[0,1] = bottomH
vertsH[1,0] = left
vertsH[1,1] = topH
vertsH[2,0] = right
vertsH[2,1] = topH
vertsH[3,0] = right
vertsH[3,1] = bottomH

rectPathH = path.Path(vertsH, codesH)
patch = patches.PathPatch(rectPathH, facecolor='red', edgecolor='red', alpha=0.5)
ax1.add_patch(patch)

fig.tight_layout()

##########################################
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
            util.append(uHighH[m])
    if e<e1:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aH*e - costH[n]])
        xlabels  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)
    elif e1<=e<eHstar:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aH*e - costH[n]])
        xlabels  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)
    elif eHstar<=e<eHmax:
        ax1.set_xticks([eHstar,eRange[n]])
        ax1.set_yticks([0,uHstar,aH*e - costH[n]])
        xlabels  = ['$e_H^*$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(e_H^*)$','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)
    else:
        ax1.set_xticks([eHstar,eHmax,eRange[n]])
        ax1.set_yticks([0,uHstar,aH*e - costH[n]])
        xlabels  = ['$e_H^*$','$\\bar{e}_{max}$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabels  = ['','$u_H(e_H^*)$','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)


    if e<=eHmax:

        leftH = 0
        rightH = e
        vertsH[0,0] = leftH
        vertsH[1,0] = leftH
        vertsH[2,0] = rightH
        vertsH[3,0] = rightH
    
    eRange1=eRange[0:n]
    util1 = util[:n]
    eRange2=eRange[n:]
    util2 = util[n:]
    eRange3=eRange[n]
    util3=util[n]
    # fig.savefig("%d.png"%z)
    z+=1
    if n==len(eRange)-1:
        n=0
        n = len(eRange)-1
    else:
        n+=1
    
    ax1.set_xticklabels(xlabels,fontsize=20)
    ax1.set_yticklabels(ylabels,fontsize=20)
    line1.set_data(eRange1, util1)
    line2.set_data(eRange2, util2)
    line3.set_data(eRange3, util3)
    return line1,line2,line3

ani = animation.FuncAnimation(fig, run, eRange, blit=False,repeat=True,interval=1)
ani.save('../video/signalingSeparatingHigh.mp4',writer=writer)
plt.show()

# Convert the mp4 video to ogg format
makeOgg = 'ffmpeg -i ../video/signalingSeparatingHigh.mp4 -c:v libtheora -c:a libvorbis -q:v 6 -q:a 5 ../video/signalingSeparatingHigh.ogv'
subprocess.call(makeOgg,shell=True)