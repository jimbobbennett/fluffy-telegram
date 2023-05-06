import { NextApiHandler, NextApiRequest, NextApiResponse } from "next";

const getBearerToken = (req: NextApiRequest) => {
  const authorizationHeader =
    req.headers instanceof Headers
      ? req.headers.get("authorization")
      : req.headers?.authorization;

  const authorizationHeaderParts = authorizationHeader?.split(" ");

  const bearerToken =
    authorizationHeaderParts?.[0]?.toLowerCase() === "bearer" &&
    authorizationHeaderParts?.[1];

  return bearerToken;
};

const validateToken = async (token: string) => {
  const result = false;

  if (token) {
    const SERVICEURL = `https://authn.${process.env.NEXT_PUBLIC_PANGEA_DOMAIN}/v1/client/token/check`;
    try {
      const response = await fetch(SERVICEURL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${process.env.AUTHN_SERVICE_TOKEN || ""}`,
        },
        body: JSON.stringify({ token: token }),
      });

      const responseJSON = await response.json();

      return responseJSON.status === "Success";
    } catch (error) {
      console.error("Error:", error);
    }
  }
  return result;
};

export const withAPIAuthentication = (apiHandler: NextApiHandler) => {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    const isTokenValid = await validateToken(getBearerToken(req));

    // Authentication failed, return 401
    if (!isTokenValid) {
      return new Response("Unauthorized", { status: 401 });
    }

    // We are good to continue
    return await apiHandler(req, res);
  };
};
