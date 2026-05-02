// eslint-disable  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZDA1WllRPT06MDg4NzM0ZjM=

import { Client } from "@langchain/langgraph-sdk";
// TODO  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZDA1WllRPT06MDg4NzM0ZjM=

export function createClient(apiUrl: string, apiKey: string | undefined) {
  return new Client({
    apiKey,
    apiUrl,
  });
}
