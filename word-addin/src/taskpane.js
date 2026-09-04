Office.onReady((info) => {
    if (info.host === Office.HostType.Word) {
        document.getElementById("process-btn").onclick = processSelection;
    }
});

async function processSelection() {
    const statusBox = document.getElementById("status");
    const btn = document.getElementById("process-btn");
    
    try {
        btn.disabled = true;
        statusBox.innerText = "Reading selection...";
        
        let textToProcess = "";
        
        await Word.run(async (context) => {
            const selection = context.document.getSelection();
            selection.load("text");
            await context.sync();
            textToProcess = selection.text;
        });
        
        if (!textToProcess.trim()) {
            statusBox.innerText = "Please select some text first.";
            btn.disabled = false;
            return;
        }

        statusBox.innerText = "Starting CANDO pipeline...";

        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8765';
        const response = await fetch(`${apiUrl}/api/text/cando`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: textToProcess })
        });
        
        if (!response.body) throw new Error("No response body");
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let finalResult = null;

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n').filter(Boolean);
            
            for (const line of lines) {
                const data = JSON.parse(line);
                statusBox.innerText = `Step: ${data.step}`;
                if (data.step === "Done" && data.result) {
                    finalResult = data.result.result;
                }
            }
        }
        
        if (finalResult) {
            statusBox.innerText = "Writing back to document...";
            await Word.run(async (context) => {
                const selection = context.document.getSelection();
                selection.insertText(finalResult, Word.InsertLocation.replace);
                await context.sync();
            });
            statusBox.innerText = "Success! Selection updated.";
        }
        
    } catch (error) {
        console.error(error);
        statusBox.innerText = `Error: ${error.message}`;
    } finally {
        btn.disabled = false;
    }
}
