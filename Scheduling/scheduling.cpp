# include <iostream>
# include <vector>
# include <queue>
# include <functional>
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

void nextPeriod( taskTime & readylist ) {
    if ( INT32_MAX - readylist.period <= readylist.deadline.first ) {
        readylist.deadline.first -= INT32_MAX ;
        readylist.deadline.second ++ ;
        readylist.deadline.first += readylist.period ;
    } // if
    else {
        readylist.deadline.first += readylist.period ;
    }

    readylist.current = readylist.excution ;
} //

pair<int,int> addBigNumberTaskTime( pair<int,int> time, int excutionTime ) {
    if ( INT32_MAX - excutionTime <= time.first ) {
        time.first -= INT32_MAX ;
        time.second ++ ;
        time.first += excutionTime ;
    } // if
    else {
        time.first += excutionTime ;
    }
    return time ;
} // addBigNumberTaskTime

int minusBigNumberTime( pair<int,int> & time, pair<int,int> & newtime ) {
    if ( time.second != newtime.second ) {
        return INT32_MAX - time.first + newtime.first ; 
    } // if
    return newtime.first - time.first ;
} // minusBigNumberTime

bool checkFinishCondition( vector<taskTime> & tasks, int size) { // check next_period time is the same
    if ( tasks.size() != size )
        return false ;
    for ( int i = 1 ; i < tasks.size() ; i ++ ) {
        if (tasks[i-1].deadline.first != tasks[i].deadline.first || tasks[i-1].deadline.second != tasks[i].deadline.second )
            return false ;
    } // for
    return true ;
} // checkFinishCondition

pair<int,int> findMinDeadline( vector<taskTime> & readylist, pair<int,int> min ) {
    for ( auto i : readylist ) {
        if ( i.deadline.second < min.second )
            min = i.deadline ;
        else if ( i.deadline.second == min.second && i.deadline.first < min.first ) {
            min = i.deadline ;
        }
    }

    return min ;
} // findLeastDeadline

auto deadline_compare = [](const taskTime& p1, const taskTime& p2) {
    if ( p1.deadline == p2.deadline  )
        return p1.index > p2.index ;

    return p1.deadline > p2.deadline;
};

auto rate_compare = [](const taskTime& p1, const taskTime& p2) {
    if ( float(p1.current)/p1.period == float(p2.current)/p2.period ) 
        return p1.index > p2.index ;

    return float(p1.current)/p1.period < float(p2.current)/p2.period ;
};

class Compare {
public:
    bool operator()(const taskTime& p1, const taskTime& p2) {
        return comp(p1, p2);
    }
    
    function<bool(const taskTime&, const taskTime&)> comp;
};

void Schedule( vector<vector<int> > & task, int & Display, int & type ) {
    // cout << "Scheduler Begin" << endl ;
    vector<taskTime> readylist ; // { index, excutionTime, period, current, deadline}
    taskTime task_current ;
    taskTime task_pre ;
    priority_queue<taskTime, vector<taskTime>, Compare> pqueue;

    if ( type == 1 ) {
        pqueue = priority_queue<taskTime, vector<taskTime>, Compare>(Compare{deadline_compare});
    }
    else if ( type == 0 ) {
        // cout << "rate _ compare" ;
        pqueue = priority_queue<taskTime, vector<taskTime>, Compare>(Compare{rate_compare});
    }
    // priority queue
    bool start = true ;
    int preempted = 0 ;
    int  taskaction_pre = -1, taskaction_current  = 0 ; // task action: start:0, end:1, preempted2, resume:3
    pair<int,int> time = {0,0}, outputtime = {0,0} ;
    pqueue.push(taskTime( 0, task[0][0], task[0][1], task[0][0], pair<int,int>(task[0][1],0 )) ) ;
    // push 1st task to queue

    while( !checkFinishCondition(readylist, task.size()) || ! pqueue.empty() ) { // 
        // cout << "Time: " << time.first << " " << time.second << " Readylist length: " << readylist.size() << " pqueue: " << pqueue.size() << endl ;
        
        outputtime = time ;
        taskTime newtask ; 
        if ( pqueue.size() != 0) {
            newtask = pqueue.top() ; 
            pqueue.pop() ;
        }
        task_pre = task_current ;
        task_current = newtask ;
        if ( task_pre.index != -1 && task_pre.current == 0 )  
            taskaction_pre = 1 ;
        else if ( task_pre.index != -1 && task_pre.current != 0 && task_current.index != task_pre.index ) {
            taskaction_pre = 2 ;
            preempted ++ ;
        }

        if ( task_current.current != task_current.excution )
            taskaction_current = 3 ;
        else if ( task_current.current == task_current.excution ) 
            taskaction_current = 0 ;

        pair<int,int> temptime = addBigNumberTaskTime( time, task_current.current ) ;
        if ( task_current.index == -1 ) {
            pair<int,int> minDeadline = findMinDeadline( readylist, {INT32_MAX,INT32_MAX} ) ;
            for ( int k = 0 ; k < readylist.size() ; k ++ ) {
                if ( minDeadline.first == readylist[k].deadline.first && minDeadline.second == readylist[k].deadline.second ) {
                    nextPeriod( readylist[k] ) ;
                    pqueue.push( readylist[k] ) ;
                    readylist.erase(readylist.begin()+k ) ;
                    k -- ;
                }
            } // for
            time = minDeadline ;
        } // if
        else if ( !readylist.empty()) { // check period condition
            pair<int,int> minDeadline = findMinDeadline( readylist, temptime ) ; // find time less than temptime
            for ( int k = 0 ; k < readylist.size() ; k ++ ) {
                if ( minDeadline.first == readylist[k].deadline.first && minDeadline.second == readylist[k].deadline.second ) {
                    nextPeriod( readylist[k] ) ;
                    pqueue.push( readylist[k] ) ;
                    readylist.erase(readylist.begin()+k ) ;
                    k -- ;
                }
            } // for
            task_current.current = task_current.current - minusBigNumberTime( time, minDeadline ) ; 
            time = minDeadline ;
                
            if ( task_current.current == 0 ) {
                readylist.push_back( task_current ) ;
            } // if
            else {
                pqueue.push( task_current ) ;
            } // else
        } // if
        else {
            task_current.current = 0 ;
            time = temptime ;
            readylist.push_back( task_current ) ;
        } // else

        

        if ( outputtime.first == 0 && outputtime.second == 0 ) { 
            for ( int i = 1 ; i < task.size() ; i ++ ) {
                pqueue.push(taskTime( i, task[i][0], task[i][1], task[i][0], pair<int,int>(task[i][1],0 )) ) ;
            } // for
        } // if

        // output
        if ( Display == 1 ) {
            if ( task_pre.index != task_current.index ) { // idle, no event
                // cout << outputtime.second << " + " << outputtime.first << " " ;
                cout << long(outputtime.second)*INT32_MAX + outputtime.first << " " ;
                if ( task_pre.index != -1) {
                    cout << task_pre.index+1 << " " << taskaction_pre << " " ;
                } // if
                cout << task_current.index+1 << " " << taskaction_current << endl ;
            }
        } // if

    } // while
    // cout << time.second << " + " << time.first << " " << task_current.index+1 << " " << "1" << endl ;
    if ( Display == 1)
        cout << long(time.second)*INT32_MAX + time.first << " " << task_current.index+1 << " " << "1" << endl ;
    // cout << " Total Time " << time.first+1 << "+ " << time.second << " Preempted " << preempted << " Finished" << endl ;
    cout << long(time.second)*INT32_MAX + time.first+1 << " " << preempted <<  endl ;
} // Schedule


int main(int argc, char const *argv[])
{

    int R ;
    int S, D, N ;
    vector<vector<int> > task ;
    // cout << "Scheduling Begin" << endl ;
    cin >> R ;
    for ( int run = 0 ; run < R ; run ++ ) {
        cout << run+1 << endl ;
        cin >> S >> D >> N ;
        for ( int i = 0 ; i < N ; i ++ ) {
            int value1,value2 ;
            cin >> value1 >> value2 ;
            task.push_back({value1,value2}) ;
        } // for
        Schedule( task, D, S ) ;



        task.clear() ;
    } // for

    return 0;
}
