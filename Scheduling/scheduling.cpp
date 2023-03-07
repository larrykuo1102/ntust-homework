# include <iostream>
# include <fstream>
# include <vector>
using namespace std ;


void EDF( vector<vector<int>> task, int Display ) {
    cout << "EDF Begin" << endl ;

} //

void RMS( vector<vector<int>> task, int Display ) {
    cout << "RMS Begin" << endl ;
} //

int main(int argc, char const *argv[])
{
    ifstream file ;
    int R ;
    int S, D, N ;
    vector<vector<int>> task ;
    file.open("./sample/input1") ;
    if ( file.fail() ) {
        cout << "open failed" << endl ;
    } // if
    cout << "Scheduling Begin" << endl ;
    file >> R ;
    cout << "Total " << R << "runs." << endl ;
    for ( int run ; run < R ; run ++ ) {
        cout << run << endl ;
        file >> S >> D >> N ;
        for ( int i = 0 ; i < N ; i ++ ) {
            vector<int> temp ;
            int value ;
            file >> value ;
            temp.push_back(value) ;
            file >> value ;
            temp.push_back(value) ;
            task.push_back(temp) ;
        } // for

        if ( S == 0 ) {
            EDF( task, D ) ;
        } // if
        else if ( S == 1) {
            RMS( task, D ) ;
        } // else if
        else {
            cout << "Type Error" ;
        } // else



        task.clear() ;
    } // for




    file.close() ;
    return 0;
}
