from __future__ import division
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.path as path
import subprocess


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
eStep = 0.05
# eStep=0.05

eRange = np.arange(eMin-eStep,eMax+eStep-0.0001,eStep)

#High type
eHstar = aL/2/cH
uHstar = aL*eHstar-cH*eHstar**2

coeffsH = [-cH,aBar,-uHstar]
eHmax = np.max(np.roots(coeffsH))

costH = cH*eRange**2
uLowH = aL*eRange-costH
uHighH= aBar*eRange-costH

yMinH,yMaxH = -10,27

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
ax1 = fig.add_subplot(2, 1, 1)
ax1.grid()
plt.plot(eRange,uHighH,'--',lw=2)
plt.plot(eRange,uLowH,'--',lw=2)
lineH1, = ax1.plot([], [],'k', lw=3)
lineH2, = ax1.plot([], [],'k', lw=3)
lineH3, = ax1.plot([], [],'ok', lw=4)
lineH4, = ax1.plot([], [],'ok', lw=4,markerfacecolor='none')
ax1.set_ylim(yMinH,yMaxH)
# ax1.set_xlabel('Level of education ($e$)')
ax1.set_ylabel('Utility ($u_H$)')
plt.legend(['$\\bar{a}e - k_H e^2$','$a_L e - k_H e^2$','$u_H(e)$'],loc='lower left',ncol=3,fontsize=20)
ax1.set_title('Type H Worker',fontsize=20)

# Initialize the shaded rectangle
leftH = 0
rightH = 0
bottomH = yMinH
topH = bottomH - yMinH + yMaxH

nverts = 5
vertsH = np.zeros((nverts, 2))
codesH = np.ones(nverts, int) * path.Path.LINETO
codesH[0] = path.Path.MOVETO
codesH[4] = path.Path.CLOSEPOLY
vertsH[0,0] = leftH
vertsH[0,1] = bottomH
vertsH[1,0] = leftH
vertsH[1,1] = topH
vertsH[2,0] = rightH
vertsH[2,1] = topH
vertsH[3,0] = rightH
vertsH[3,1] = bottomH

rectPathH = path.Path(vertsH, codesH)
patchH = patches.PathPatch(rectPathH, facecolor='red', edgecolor='red', alpha=0.5)
ax1.add_patch(patchH)




ax2 = fig.add_subplot(2, 1, 2)
ax2.grid()
plt.plot(eRange,uHighL,'--',lw=2)
plt.plot(eRange,uLowL,'--',lw=2)
lineL1, = ax2.plot([], [],'k', lw=3)
lineL2, = ax2.plot([], [],'k', lw=3)
lineL3, = ax2.plot([], [],'ok', lw=4)
lineL4, = ax2.plot([], [],'ok', lw=4,markerfacecolor='none')
ax2.set_ylim(yMinL,yMaxL)
ax2.set_xlabel('Level of education ($e$)')
ax2.set_ylabel('Utility ($u_L$)')
plt.legend(['$\\bar{a}e - k_L e^2$','$a_L e - k_L e^2$','$u_L(e)$'],loc='lower left',ncol=3,fontsize=20)
ax2.set_title('Type L Worker',fontsize=20)
# plt.show()


# Initialize the shaded rectangle
leftL = 0
rightL = 0
bottomL = yMinH
topL = bottomL - yMinL + yMaxL

nverts = 5
vertsL = np.zeros((nverts, 2))
codesL = np.ones(nverts, int) * path.Path.LINETO
codesL[0] = path.Path.MOVETO
codesL[4] = path.Path.CLOSEPOLY
vertsL[0,0] = leftL
vertsL[0,1] = bottomL
vertsL[1,0] = leftL
vertsL[1,1] = topL
vertsL[2,0] = rightL
vertsL[2,1] = topL
vertsL[3,0] = rightL
vertsL[3,1] = bottomL

rectPathL = path.Path(vertsL, codesL)
patchL = patches.PathPatch(rectPathL, facecolor='green', edgecolor='green', alpha=0.5)
ax2.add_patch(patchL)

#############
z,n=10000,0
def run(*args):
    global z,n

    e1 = 0.25

    e = eRange[n]
    utilH,utilL =[],[]
    for m,x in enumerate(eRange):
        if x<e:
            utilH.append(uLowH[m])
            utilL.append(uLowL[m])
        else:
            utilH.append(aBar*e - costH[m])
            utilL.append(aBar*e - costL[m])
    if e<e1:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aBar*e - costH[n]])
        xlabelsH  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsH  = ['','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        leftH = 0
        rightH = e
        vertsH[0,0] = leftH
        vertsH[1,0] = leftH
        vertsH[2,0] = rightH
        vertsH[3,0] = rightH

    elif e1<=e<eHstar:
        ax1.set_xticks([eRange[n]])
        ax1.set_yticks([0,aBar*e - costH[n]])
        xlabelsH  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsH  = ['','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        leftH = 0
        rightH = e
        vertsH[0,0] = leftH
        vertsH[1,0] = leftH
        vertsH[2,0] = rightH
        vertsH[3,0] = rightH

    elif eHstar<=e<eHmax:
        ax1.set_xticks([eHstar,eRange[n]])
        ax1.set_yticks([0,uHstar,aBar*e - costH[n]])
        xlabelsH  = ['$e_H^*$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsH  = ['','$u_H(e_H^*)$','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        leftH = 0
        rightH = e
        vertsH[0,0] = leftH
        vertsH[1,0] = leftH
        vertsH[2,0] = rightH
        vertsH[3,0] = rightH

    else:
        ax1.set_xticks([eHstar,eHmax,eRange[n]])
        ax1.set_yticks([0,uHstar,aBar*e - costH[n]])
        xlabelsH  = ['$e_H^*$','$e_H^{max}$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsH  = ['','$u_H(e_H^*)$','$u_H(\\bar{e})$'] #% np.round(eRange[n],1)

        leftH = 0
        rightH = eHmax
        vertsH[0,0] = leftH
        vertsH[1,0] = leftH
        vertsH[2,0] = rightH
        vertsH[3,0] = rightH


    if e<e1:
        ax2.set_xticks([eRange[n]])
        ax2.set_yticks([0,aBar*e - costL[n]])
        xlabelsL  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsL  = ['','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        leftL = 0
        rightL = e
        vertsL[0,0] = leftL
        vertsL[1,0] = leftL
        vertsL[2,0] = rightL
        vertsL[3,0] = rightL


    elif e1<=e<eLstar:
        ax2.set_xticks([eRange[n]])
        ax2.set_yticks([0,aBar*e - costL[n]])
        xlabelsL  = ['$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsL  = ['','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        leftL = 0
        rightL = e
        vertsL[0,0] = leftL
        vertsL[1,0] = leftL
        vertsL[2,0] = rightL
        vertsL[3,0] = rightL


    elif eLstar<=e<eLmax:
        ax2.set_xticks([eLstar,eRange[n]])
        ax2.set_yticks([0,uLstar,aBar*e - costL[n]])
        xlabelsL  = ['$e_L^*$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsL  = ['','$u_L(e_L^*)$','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        leftL = 0
        rightL = e
        vertsL[0,0] = leftL
        vertsL[1,0] = leftL
        vertsL[2,0] = rightL
        vertsL[3,0] = rightL


    else:
        ax2.set_xticks([eLstar,eLmax,eRange[n]])
        ax2.set_yticks([0,uLstar,aBar*e - costL[n]])
        xlabelsL  = ['$e_L^*$','$e_L^{max}$','$\\bar{e}$'] #% np.round(eRange[n],1)
        ylabelsL  = ['','$u_L(e_L^*)$','$u_L(\\bar{e})$'] #% np.round(eRange[n],1)

        leftL = 0
        rightL = eLmax
        vertsL[0,0] = leftL
        vertsL[1,0] = leftL
        vertsL[2,0] = rightL
        vertsL[3,0] = rightL
    

    eRange1=eRange[0:n]
    utilH1 = utilH[:n]
    utilL1 = utilL[:n]
    eRange2=eRange[n:]
    utilH2 = utilH[n:]
    utilL2 = utilL[n:]
    eRange3=eRange[n]
    utilH3=utilH[n]
    utilH4=uLowH[n]
    utilL3=utilL[n]
    utilL4=uLowL[n]
    # fig.savefig("%d.png"%z)
    z+=1
    if n==len(eRange)-1:
        n=0
        n = len(eRange)-1
    else:
        n+=1
    
    ax1.set_xticklabels(xlabelsH,fontsize=20)
    ax1.set_yticklabels(ylabelsH,fontsize=20)
    ax2.set_xticklabels(xlabelsL,fontsize=20)
    ax2.set_yticklabels(ylabelsL,fontsize=20)
    ax1.set_xlim(eMin, eMax)
    ax1.set_ylim(yMinH,yMaxH)
    ax2.set_xlim(eMin, eMax)
    ax2.set_ylim(yMinL,yMaxL)
    lineH1.set_data(eRange1, utilH1)
    lineH2.set_data(eRange2, utilH2)
    lineH3.set_data(eRange3, utilH3)
    lineH4.set_data(eRange3, utilH4)
    lineL1.set_data(eRange1, utilL1)
    lineL2.set_data(eRange2, utilL2)
    lineL3.set_data(eRange3, utilL3)
    lineL4.set_data(eRange3, utilL4)
    return lineH1,lineH2,lineH3,lineH4,lineL1,lineL2,lineL3,lineL4

ani = animation.FuncAnimation(fig, run, eRange, blit=False,repeat=True,interval=1)
ani.save('../video/signalingPooling.mp4',writer=writer)
plt.show()


# makegif = 'convert -loop 0 *.png Solow_Animated.gif'
# subprocess.call(makegif,shell=True)

# Convert the mp4 video to ogg format
makeOgg = 'ffmpeg -i ../video/signalingPooling.mp4 -c:v libtheora -c:a libvorbis -q:v 6 -q:a 5 ../video/signalingPooling.ogv'
subprocess.call(makeOgg,shell=True)
