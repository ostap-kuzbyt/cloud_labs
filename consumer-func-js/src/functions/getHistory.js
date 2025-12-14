const { app } = require('@azure/functions');
const cosmosService = require('../services/cosmosService');

app.http('getHistory', {
    methods: ['GET'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        const deviceId = request.query.get('deviceId');

        if (!deviceId) {
            return {
                status: 400,
                body: "Please pass a deviceId on the query string"
            };
        }

        try {
            const history = await cosmosService.getHistory(deviceId);
            return {
                status: 200,
                jsonBody: history
            };
        } catch (err) {
            context.log.error("Error getting history:", err);
            return {
                status: 500,
                body: "Internal Server Error"
            };
        }
    }
});
