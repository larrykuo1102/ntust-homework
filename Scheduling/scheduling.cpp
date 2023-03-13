# include <iostream>
# include <vector>
# include <queue>
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
    vector<vector<int> > readylist ; // { index, excutionTime, period}
    vector<int> currenttask, outputtask ;
    priority_queue<vector<int>, vector<vector<int>>, Compare> pqueue;

    if ( type == 0 ) {
        pqueue = priority_queue<vector<int>, vector<vector<int>>, Compare>(Compare{deadline_compare});
    }
    else if ( type == 1 ) {
        pqueue = priority_queue<vector<int>, vector<vector<int>>, Compare>(Compare{rate_compare});
    }
    // priority queue
    bool start = true ;
    int time = 0, taskaction_output, taskaction_current  = 0 ;
    // push task to queue
    // erase from readylist 
    while(! currenttask.empty() || ! pqueue.empty() ) { // 
        outputtask = currenttask ;
        // get task
        vector<int> newtask ; 
        currenttask = newtask ;
        // do task
        // push to priority queue :
        //      if task not done push into queue
        //      if the task done -> push into readylist
        //      or if period of task arrived then push into queue
        //      ( from readylist )

        // output
        if ( Display == 1 ) {
            cout << time << " " ;
            if ( !outputtask.empty()) {
                cout << outputtask[1] << " " << taskaction_output << endl ;
            } // if
            cout << currenttask[1] << " " << taskaction_current << endl ;
        } // if
        time ++ ;
    } // while

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
