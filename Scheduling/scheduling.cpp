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
    int current ; // remain excution time
    pair<int,int> deadline ; // deadline or next period begin
    taskTime(int index,int excution,int period, int current, pair<int,int> deadline) : index(index),excution(excution), period(period),
        current(current),deadline(deadline) {}
    taskTime():index(-1){}
}; 

void addBigNumber( pair<int,int> & time ) {
    if ( time.first +1 == INT32_MAX ) {
        time.second ++ ;
        time.first = 0 ;
    }   
    else 
        time.first ++ ;
} // bigNumber

void addBigNumberDeadline( pair<int,int> & time, int period ) {
    if ( INT32_MAX - period <= time.first ) {
        time.first -= INT32_MAX ;
        time.second ++ ;
        time.first += period ;
    } // if
    else {
        time.first += period ;
    }
} //

bool checkFinishCondition( vector<taskTime> & tasks, int size) { // check next_period time is the same
    if ( tasks.size() != size )
        return false ;
    for ( int i = 1 ; i < tasks.size() ; i ++ ) {
        if (tasks[i-1].deadline.first != tasks[i].deadline.first || tasks[i-1].deadline.second != tasks[i].deadline.second )
            return false ;
    } // for

    cout << "over!!!!" << endl ;
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
    taskTime currenttask ;
    taskTime outputtask ;
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
        pqueue.push(taskTime( i, task[i][0], task[i][1], task[i][0], pair<int,int>(task[i][1],0 )) ) ;
    } // for
    // push task to queue
    cout << "push task to queue" << endl ;
    // erase from readylist 

    // checkFinishCondition(readylist) -> bool
    // while( readylist.size()!= task.size() || ! pqueue.empty() ) { // 
    while( !checkFinishCondition(readylist, task.size()) || ! pqueue.empty() ) { // 
        // cout << "Time: " << time.first << " Readylist length: " << readylist.size() << " pqueue: " << pqueue.size() << endl ;
        outputtask = currenttask ;
        if ( outputtask.index != -1 && outputtask.current == 0 ) 
            taskaction_output = 1 ;
        else if ( outputtask.index != -1 && outputtask.current != 0  ) {
            taskaction_output = 2 ;
            preempted ++ ;
        }

        // get task
        taskTime newtask = pqueue.top() ; 
        pqueue.pop() ;
        // cout << "test " << pqueue.size() << endl ;
        currenttask = newtask ;
        if ( currenttask.current != currenttask.excution )
            taskaction_current = 3 ;
        else if ( currenttask.current == currenttask.excution ) 
            taskaction_current = 0 ;
        // do task
        currenttask.current -- ;
        if ( currenttask.current > 0 ) {
            pqueue.push( currenttask ) ;
        } // if
        else if ( currenttask.current == 0 ) {
            int tempindex = currenttask.excution ;
            readylist.push_back( currenttask ) ;
        }

        // if time == deadline
        if ( !readylist.empty()) { // check period condition
            for ( int k = 0 ; k < readylist.size() ; k ++ ) {
                if ( time.first == readylist[k].deadline.first && time.second == readylist[k].deadline.second ) {
                    addBigNumberDeadline( readylist[k].deadline, readylist[k].period ) ;
                    readylist[k].current = readylist[k].excution ;
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
            if ( outputtask.index != currenttask.index ) { // idle, no event
                cout << time.first << " + " << time.second << " " ;
                if ( outputtask.index != -1) {
                    cout << outputtask.index+1 << " " << taskaction_output << " " ;
                } // if
                cout << currenttask.index+1 << " " << taskaction_current << endl ;
            }
        } // if

        addBigNumber(time) ;
    } // while

    cout << " Total Time " << time.first+1 << "+ " << time.second << " Preempted " << preempted << " Finished" << endl ;
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
