// server.js
const express = require('express');
const LangflowClient = require('./langflowClient');
const config = require('./config');
const cors = require('cors');
const app = express();
const { spawn } = require('child_process');



app.use(cors({
    origin: 'https://atmaveda.vercel.app', // Replace with your frontend URL
  }));
app.use(cors())
app.use(express.json());

// Initialize LangFlow client
const langflowClient = new LangflowClient(
    config.LANGFLOW_BASE_URL,
    config.APPLICATION_TOKEN
);

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'OK' });
});

// Main API endpoint for processing messages
app.post('/api/chatbot', async (req, res) => {
    try {
        const { 
            message, 
            inputType = 'chat', 
            outputType = 'chat', 
            stream = false 
        } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required'});
        }

        const response = await langflowClient.runFlow(
            config.FLOW_ID,
            config.LANGFLOW_ID,
            message,
            inputType,
            outputType,
            config.TWEAKS,
            stream,
            (data) => console.log("Received:", data.chunk),
            (message) => console.log("Stream Closed:", message),
            (error) => console.log("Stream Error:", error)
        );

        if (!stream && response && response.outputs) {
            const output = response.outputs[0].outputs[0].outputs.message;
            return res.json({ response: output.message.text });
        }

        // Handle streaming response
        if (stream) {
            // Set headers for SSE
            res.writeHead(200, {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            });

            // Handle streaming data
            response.on('data', (chunk) => {
                res.write(`data: ${JSON.stringify(chunk)}\n\n`);
            });

            response.on('end', () => {
                res.end();
            });
        }

    } catch (error) {
        console.error('Error processing request:', error);
        res.status(500).json({ error: 'Internal server error', details: error.message });
    }
});


//personalized recomendation
app.post('/api/pr', async (req, res) => {
    try {
        const { 
            message, 
            inputType = 'chat', 
            outputType = 'chat', 
            stream = false 
        } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        const response = await langflowClient.runFlow(
            config.FLOW_ID,
            config.LANGFLOW_ID,
            message,
            inputType,
            outputType,
            config.TWEAKS,
            stream,
            (data) => console.log("Received:", data.chunk),
            (message) => console.log("Stream Closed:", message),
            (error) => console.log("Stream Error:", error)
        );

        if (!stream && response && response.outputs) {
            const output = response.outputs[0].outputs[0].outputs.message;
            return res.json({ response: output.message.text });
        }

        // Handle streaming response
        if (stream) {
            // Set headers for SSE
            res.writeHead(200, {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            });

            // Handle streaming data
            response.on('data', (chunk) => {
                res.write(`data: ${JSON.stringify(chunk)}\n\n`);
            });

            response.on('end', () => {
                res.end();
            });
        }

    } catch (error) {
        console.error('Error processing request:', error);
        res.status(500).json({ error: 'Internal server error', details: error.message });
    }
});

//horoscope
app.post('/api/horoscope', async (req, res) => {
    try {
        const { 
            message, 
            inputType = 'chat', 
            outputType = 'chat', 
            stream = false 
        } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        const response = await langflowClient.runFlow(
            config.FLOW_ID,
            config.LANGFLOW_ID,
            message,
            inputType,
            outputType,
            config.TWEAKS,
            stream,
            (data) => console.log("Received:", data.chunk),
            (message) => console.log("Stream Closed:", message),
            (error) => console.log("Stream Error:", error)
        );

        if (!stream && response && response.outputs) {
            const output = response.outputs[0].outputs[0].outputs.message;
            return res.json({ response: output.message.text });
        }

        // Handle streaming response
        if (stream) {
            // Set headers for SSE
            res.writeHead(200, {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            });

            // Handle streaming data
            response.on('data', (chunk) => {
                res.write(`data: ${JSON.stringify(chunk)}\n\n`);
            });

            response.on('end', () => {
                res.end();
            });
        }

    } catch (error) {
        console.error('Error processing request:', error);
        res.status(500).json({ error: 'Internal server error', details: error.message });
    }
});



//sudarsh edit

app.post('/generate-kundali', (req, res) => {
    const { date, time, place, gender, timezone, lagna_file, navamsa_file } = req.body;

    let responseSent = false;

    const pythonProcess = spawn('python', [
        'generate_kundali.py',
        date,
        time,
        place,
        gender,
        timezone,
        lagna_file || "lagna_chart.svg",
        navamsa_file || "navamsa_chart.svg"
    ]);

    let result = '';

    pythonProcess.stdout.on('data', (data) => {
        result += data.toString(); // Collect the JSON output from Python
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
        if (!responseSent) {
            res.status(500).send(`Error generating Kundali: ${data}`);
            responseSent = true;
        }
    });

    pythonProcess.on('close', (code) => {
        if (!responseSent) {
            if (code === 0) {
                try {
                    // Parse the JSON output from Python
                    const { analysis, lagna_file, navamsa_file } = JSON.parse(result);

                    // Read the SVG files
                    const lagnaSvg = fs.readFileSync(path.resolve(__dirname, lagna_file), 'utf8');
                    const navamsaSvg = fs.readFileSync(path.resolve(__dirname, navamsa_file), 'utf8');

                    // Send the response with analysis and SVG files
                    res.status(200).json({
                        message: "Charts saved successfully.",
                        analysis: analysis,
                        lagna_svg: lagnaSvg,
                        navamsa_svg: navamsaSvg
                    });
                } catch (error) {
                    console.error('Error parsing Python output or reading SVG files:', error);
                    res.status(500).send('Failed to process the result.');
                }
            } else {
                res.status(500).send('Failed to generate Kundali charts.');
            }
            responseSent = true;
        }
    });
});




// Start the server
app.listen(config.PORT, () => {
    console.log(`Server running on port ${config.PORT}`);
});
