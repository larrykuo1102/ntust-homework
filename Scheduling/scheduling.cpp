# include <iostream>
# include <vector>
# include <queue>
# include <functional>
# include <unordered_map>
using namespace std ;

struct taskTime {
    int index ;
    int excution ;
    int period ;
    pair<int,int> current ;
    pair<int,int> deadline ;
}; 

int addBigNumber( pair<int,int> time ) {
    if ( time.first +1 == INT_MAX ) {
        time.second ++ ;
        time.first = 0 ;
    }
     
} // bigNumber

bool checkFinishCondition( vector<taskTime> & tasks) { // check next_period time is the same
    for ( int i = 1 ; i < tasks.size() ; i ++ ) {
        if (tasks[i-1].deadline.first != tasks[i].deadline.first || tasks[i-1].deadline.second != tasks[i].deadline.second )
            return false ;
    } // for

    return true ;
} // checkFinishCondition

auto deadline_compare = [](const taskTime& p1, const taskTime& p2) {
    return p1.deadline > p2.deadline;
};

auto rate_compare = [](const taskTime& p1, const taskTime& p2) {
    return p1.excution/p1.period > p2.excution/p2.period;
};

class Compare {
public:
    bool operator()(const taskTime& p1, const taskTime& p2) {
        return comp(p1, p2);
    }
    
    function<bool(const taskTime&, const taskTime&)> comp;
};

void Schedule( vector<vector<int> > task, int Display, int type ) {
    cout << "Scheduler Begin" << endl ;
    cout << task[0][1] << " " << task[1][1] << endl ;
    vector<taskTime> readylist ; // { index, excutionTime, period, current, deadline}
    // vector<taskTime> readylist_map ;
    vector<int> currenttask, outputtask ;
    priority_queue<taskTime, vector<taskTime>, Compare> pqueue;
    // priority_queue<vector<taskTime>, vector<vector<taskTime>>, Compare> pqueue;

    if ( type == 0 ) {
        pqueue = priority_queue<taskTime, vector<taskTime>, Compare>(Compare{deadline_compare});
    }
    else if ( type == 1 ) {
        pqueue = priority_queue<taskTime, vector<taskTime>, Compare>(Compare{rate_compare});
    }
    cout << "Success declare priority queue" << endl ;
    // priority queue
    bool start = true ;
    int preempted = 0 ;
    int  taskaction_output = -1, taskaction_current  = 0 ; // task action: start, 0, end, 1, preempted, 2, resume, 3
    pair<int,int> time ;
    for ( int i = 0 ; i < task.size() ; i ++ ) {
        pqueue.push({i,task[i][0],task[i][1], task[i][0],task[i][1]}) ;
    } // for
    // push task to queue
    cout << "push task to queue" << endl ;
    // erase from readylist 
    // checkFinishCondition() -> bool
    while( readylist.size()!= task.size() || ! pqueue.empty() ) { // 
        // cout << "Time: " << time << " Readylist length: " << readylist.size() << " pqueue: " << pqueue.size() << endl ;
        outputtask = currenttask ;
        if ( ! outputtask.empty() && outputtask[3] == 0 ) 
            taskaction_output = 1 ;
        else if ( ! outputtask.empty() && outputtask[3] != 0  ) {
            taskaction_output = 2 ;
            preempted ++ ;
        }

        // get task
        vector<int> newtask = pqueue.top() ; 
        pqueue.pop() ;
        // cout << "test " << pqueue.size() << endl ;
        currenttask = newtask ;

        if ( newtask[3] != newtask[1] )
            taskaction_current = 3 ;
        else if ( newtask[3] == newtask[1] ) 
            taskaction_current = 0 ;
        // do task
        newtask[3] -- ;
        if ( newtask[3] > 0 ) {
            pqueue.push( newtask ) ;
        } // if
        else if ( newtask[3] == 0 ) {
            int tempindex = newtask[0] ;
            readylist.push_back( { tempindex, task[tempindex][0], task[tempindex][1], task[tempindex][0], task[tempindex][4] }) ;
        }
        
        if ( !readylist.empty()) { // check period condition
            for ( int k = 0 ; k < readylist.size() ; k ++ ) {
                if ( timefront % readylist[k][2] == 0 ) {
                    pqueue.push( readylist[k] ) ;
                    readylist.erase(readylist.begin()+k ) ;
                    k -- ;
                }
            }
        } // else if
        // push to priority queue :
        //      if task not done push into queue
        //      if the task done -> push into readylist
        //      or if period of task arrived then push into queue
        //      ( from readylist )

        // output
        if ( Display == 1 ) {
            cout << timefront << " " ;
            if ( !outputtask.empty()) {
                cout << outputtask[1] << " " << taskaction_output << " " ;
            } // if
            cout << currenttask[1] << " " << taskaction_current << endl ;
        } // if

        addbigNumber(time) ;
    } // while

    cout << " Total Time " << timefront+1 << " Preempted " << preempted << " Finished" << endl ;
} //

// calculate deadline
// big number
// next period

int main(int argc, char const *argv[])
{

    int R ;
    int S, D, N ;
    vector<vector<int> > task ;
    cout << "Scheduling Begin" << endl ;
    cin >> R ;
    cout << "Total " << R << "runs." << endl ;
    for ( int run = 0 ; run < R ; run ++ ) {
        cout << run << endl ;
        cin >> S >> D >> N ;
        for ( int i = 0 ; i < N ; i ++ ) {
            int value1,value2 ;
            cin >> value1 >> value2 ;
            task.push_back({value1,value2}) ;
        } // for
        Schedule( task, D, S ) ;



        task.clear() ;
    } // for




    // file.close() ;
    return 0;
}
