package com.example.watchmonitoringapp;

import android.os.Bundle;
import android.support.wearable.activity.WearableActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends WearableActivity {

    private TextView serverCount;
    private Button toastButton;
    private ProgressBar progressBar;
    private int i = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        serverCount = findViewById(R.id.serverCount);
        toastButton = findViewById(R.id.toastButton);
        progressBar = findViewById(R.id.progressBar);

        toastButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                test_updater();
            }
        });
        // Enables Always-on
        setAmbientEnabled();
    }

    private void test_updater(){
        i += 10;
        if (i >= 110)
            i = 0;
        progressBar.setProgress( i, true);
    }
}
