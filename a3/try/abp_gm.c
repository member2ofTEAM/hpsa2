#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

//phase is not a global anymore
int t0 = -9;
int t1 = -3;
int player;
int pplayer;
int board[31];
int inf = 999999999;
int p1w[12];
int p2w[12];

int d = 49;

int w1 = 4;
int w2 = 10;
int w3 = 2;
int w4 = 1;
int w5 = 2;
int w6 = 4;

int stable1[9] = {-12, -11, -10, -9, -8, -7, -6, -5, -4};
int stab23[5] = {-7, -6, -5, -4, -3}; /* 2 - 3 are the same */
int stab4[4] = {-5, -4, -3, -2};
int stab59[3] = {-4, -3, -2}; /* 5 - 9 are the same */
int stab1012[2] = {-3, -2}; /* 10-12 are the same */


#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })



/* Right now Phase 2 ignores the new rule! */

void alpha_better();

int main(int argc, char *argv[])
{
    int i, phase;

    player = atoi(argv[1]);
    pplayer = player;
    phase = atoi(argv[2]);
    
    for (i = 3; i < 34; i++)
    {
        board[i - 3] = atoi(argv[i]);
    }
    
    
    //phase = 1;
    //player = 1;
    //board[11] = 3;
    
    for (i = 0; i < 12; i++)
    {
        p1w[i] = 1;
        p2w[i] = 1;
    }

    for (i = 0; i < 31; i++)
    {
        if (board[i] > 0 && i != 11)
            p1w[board[i] - 1] = 0;   
        if (board[i] < 0)
            p2w[(-1 * board[i]) - 1] = 0; 
    }

    alpha_better(phase);

    return 0;
} /* end of main */ 

void torques(int *torque)
{
   int i, tt0 = -9, tt1 = -3;
 
   for(i = -15; i < 16; i++)
   {
       if(i < -3)
          tt0 += abs(i + 3) * abs(board[i + 15]);
       else
          tt0 -= abs(i + 3) * abs(board[i + 15]);
       if(i < -1)
          tt1 += abs(i + 1) * abs(board[i + 15]);
       else
          tt1 -= abs(i + 1) * abs(board[i + 15]);
   }

   torque[0] = tt0;
   torque[1] = tt1;
}

int tipped(int *t)
{
    return (t[0] > 0 || t[1] < 0);
}

/* Calculates a score using the current state of the board
 */
int eval_fn(int exhausted, int phase)
{
    if (exhausted)
    {
        player = -1 * player;
        return player * inf;
    }
    else
    {
        player = -1 * player;
        return 0;
    }
}

int value(int alpha, int beta, int depth, int max, int phase)
{
    int v = -inf, i, next = 0, j, *pw;
    int t[2], wleft = 0, tmp, p1wn = 0;
    
    for (i = 0; i < 12; i++)
    {
        wleft += p1w[i] + p2w[i];
    }
    if (!wleft)
    {
        phase += 1;
        p1w[0] = 2;
    }

	
    player = -1 * player;
	
    if (depth > d){
        return eval_fn(0, phase);
    }
    

    if (phase == 1)
    {
    if (player > 0)
        pw = p1w;
    else
        pw = p2w;

    for (j = 0; j < 12; j++)
    {
        if (pw[j])
            pw[j] = 0;
        else
            continue;
        for (i = 0; i < 31; i++)
        {
            if (board[i])
                continue;
            board[i] = player * (j + 1);
            torques(t);
            if(!tipped(t))
            {
                next = 1;
                if (max)
                {
                    v = max(v, value(alpha, beta, depth + 1, 0, phase));
                    if (v >= beta)
                    {
                        player = -1 * player;
                        board[i] = 0;
                        return v;
                    }
                    alpha = max(alpha, v);
                }
                else
                {
                    v = min(v, value(alpha, beta, depth + 1, 1, phase));
                    if (v <= alpha)
                    {
                        player = -1 * player;
                        board[i] = 0;
                        return v;
                    }
                    beta = min(beta, v);
                }
            }
            board[i] = 0;
         }
         pw[j] = 1;
    }
    }
    if (phase == 2)
    {
        for (i = 0; i < 31; i++)
        {
            if (board[i] > 0)
                p1wn += 1;
        }
        for (i = 0; i < 31; i++)
        {  
            if (p1wn > 0 && board[i] < 0)
                continue;
            if (!board[i])
                continue;
            tmp = board[i];
            board[i] = 0;
            torques(t);
            if(!tipped(t))
            {
                next = 1;
                if (max)
                {
                    v = max(v, value(alpha, beta, depth + 1, 0, phase)); 
                    if (v >= beta)
                    {
                        player = -1 * player;
                        board[i] = tmp;
                        return v;
                    }
                    alpha = max(alpha, v);
                }
                else
                {
                    v = min(v, value(alpha, beta, depth + 1, 1, phase));
                    if (v <= alpha)
                    {
                        player = -1 * player;
                        board[i] = tmp;
                        return v;
                    }
                    beta = min(beta, v);
                }
            }
            board[i] = tmp;
        }
    }
    if (!next)
        return eval_fn(1, phase);
    player = -1 * player;
    return v;
}
                                 
/* Recrusively realizes feasible sequences of nontipping moves and calls
 * the evaulation function
 */
void alpha_better(int phase)
{
    int best_v = -2 * inf, v = inf;
    int i, j;
    int t[2];
    int best_move[2];
    int *pw;
    int tmp;
    int p1wn = 0;
    

    if (phase == 1)
    {
    if (player > 0)
        pw = p1w;
    else
        pw = p2w;

    for (j = 0; j < 12; j++)
    {
        if(pw[j])
            pw[j] = 0;
        else
            continue;
        for (i = 0; i < 31; i++)
        {
            if (board[i])
                continue;
            board[i] = player * (j + 1);
            torques(t);
            if(!tipped(t))
            {
                v = value((-1 * inf), inf, 1, 0, phase);
                if (v > best_v)
                {
                    best_v = v;
                    best_move[0] = i;
                    best_move[1] = (player > 0) ? (j + 1) : (-1 * (j + 1));
                }
            }
            board[i] = 0;
        }
        pw[j] = 1;
    }
    }
    if (phase == 2)
    {
    for (i = 0; i < 31; i++)
    {
        if (board[i] > 0)
            p1wn += 1;
    }
    for (i = 0; i < 31; i++)
    {
        if (p1wn > 0 && board[i] < 0)
            continue;
        if (!board[i])
            continue;
        tmp = board[i];
        board[i] = 0;
        torques(t);
        if (!tipped(t))
        {
            v = value((-1 * inf), inf, 1, 0, phase);
            if (v > best_v)
            {
                best_v = v;
                best_move[0] = i;
                best_move[1] = tmp;
            }
        }
        board[i] = tmp;
    }
	}
    printf("%d %d %d\n", best_move[0], abs(best_move[1]), best_v);
}




