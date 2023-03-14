# include <iostream>
# include <vector>
# include <queue>
# include <functional>
using namespace std ;


auto deadline_compare = [](const vector<int>& p1, const vector<int>& p2) {
    return p1[1] > p2[1];
};

auto rate_compare = [](const vector<int>& p1, const vector<int>& p2) {
    return p1[1]/p1[2] > p2[1]/p2[2];
};

class Compare {
public:
    bool operator()(const vector<int>& p1, const vector<int>& p2) {
        return comp(p1, p2);
    }
    
    function<bool(const vector<int>&, const vector<int>&)> comp;
};

void Schedule( vector<vector<int> > task, int Display, int type ) {
    cout << "Scheduler Begin" << endl ;
    cout << task[0][1] << " " << task[1][1] << endl ;
    vector<vector<int> > readylist ; // { index, excutionTime, period, current}
    vector<int> currenttask, outputtask ;
    priority_queue<vector<int>, vector<vector<int>>, Compare> pqueue;

    if ( type == 0 ) {
        pqueue = priority_queue<vector<int>, vector<vector<int>>, Compare>(Compare{deadline_compare});
    }
    else if ( type == 1 ) {
        pqueue = priority_queue<vector<int>, vector<vector<int>>, Compare>(Compare{rate_compare});
    }
    cout << "Success declare priority queue" << endl ;
    // priority queue
    bool start = true ;
    int preempted = 0 ;
    int time = 0, taskaction_output = -1, taskaction_current  = 0 ; // task action: start, 0, end, 1, preempted, 2, resume, 3
    for ( int i = 0 ; i < task.size() ; i ++ ) {
        pqueue.push({i,task[i][0],task[i][1], task[i][0]}) ;
    } // for
    // push task to queue
    cout << "push task to queue" << endl ;
    // erase from readylist 
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
            readylist.push_back( { tempindex, task[tempindex][0], task[tempindex][1], task[tempindex][0] }) ;
    

        }
        
        if ( !readylist.empty()) { // check period condition
            for ( int k = 0 ; k < readylist.size() ; k ++ ) {
                if ( time % readylist[k][2] == 0 ) {
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
            cout << time << " " ;
            if ( !outputtask.empty()) {
                cout << outputtask[1] << " " << taskaction_output << " " ;
            } // if
            cout << currenttask[1] << " " << taskaction_current << endl ;
        } // if
        time ++ ;
    } // while

    cout << " Total Time " << time+1 << " Preempted " << preempted << " Finished" << endl ;
} //



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
