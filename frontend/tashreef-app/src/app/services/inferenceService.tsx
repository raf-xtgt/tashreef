export const InferenceService = {

  async generateEInvitationCard(payload: any): Promise<any> {
    const response = await fetch("http://localhost:8000/ts/pattern/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Failed to analyze draft");
    }

    return await response.json();
  },



}