#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int d, n, q;
    if (!(cin >> d >> n >> q)) return 0;

    // Handle queries
    for (int i = 0; i < q; i++) {
        if (d == 1) {
            cout << 0 << flush;
        } else if (d == 2) {
            cout << "0,0" << flush;
        } else {
            cout << "0,0,0" << flush;
        }
        cout << "\n";

        // Consume next line if possible
        string dummy;
        if (!getline(cin, dummy)) break;
    }

    // Final output depending on dimension
    if (d == 1) {
        for (int i = 0; i < n; i++) {
            if (i > 0) cout << " ";
            cout << 0;
        }
        cout << "\n";
    } else if (d == 2) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (j > 0) cout << " ";
                cout << 0;
            }
            cout << "\n";
        }
    } else { // d == 3
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    if (k > 0) cout << " ";
                    cout << 0;
                }
                cout << "\n";
            }
        }
    }

    return 0;
}
