package com.team1.arspace

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.team1.arspace.ui.theme.ArspaceTheme
import com.team1.arspace.R.layout.activity_main1

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(activity_main1)

        val toAR =findViewById<Button>(R.id.showInput2)
        toAR.setOnClickListener {
            val intent= Intent(this, MainActivity2::class.java)
            startActivity(intent)
        }

        val toRL =findViewById<Button>(R.id.showInput1)
        toRL.setOnClickListener {
            val intent= Intent(this, MainActivity3::class.java)
            startActivity(intent)
        }
    }
}

