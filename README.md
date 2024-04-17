# Demo OATH Devices

This repository is a demo application for registering, managing and using OATH authenticators for 2FA.

* Features
  * OATH registration through QR
  * Backup codes
  * Enable/Disable 2FA
  * Authorization tokens with 2fa claims

## Preview

The following screenshots are the previews in the frontend application.

### Login screen
![image](https://github.com/Grapphy/oath-devices/assets/76534455/fc5952c8-9bb0-479e-be18-cf25c4320ca3)

### Authenticator disabled

![image](https://github.com/Grapphy/oath-devices/assets/76534455/84584692-c06e-44cf-83b1-1b4b7ff662e8)

![image](https://github.com/Grapphy/oath-devices/assets/76534455/6f13ad10-c903-427a-8145-dfa52d6cf601)

![image](https://github.com/Grapphy/oath-devices/assets/76534455/d7143dcd-df55-410f-bb3e-953d52204c4e)


### Authenticator enabled

![image](https://github.com/Grapphy/oath-devices/assets/76534455/ed16a316-e17e-4b32-82a8-0bf4985cdcc4)

![image](https://github.com/Grapphy/oath-devices/assets/76534455/1328b5ac-5ddc-4a64-892d-0affec47a572)

## OpenAPI definition
The following is the OpenAPI definition for the backend

```yaml
openapi: 3.1.0
info:
  title: FastAPI
  version: 0.1.0
paths:
  '/api/v1/users/{user_id}':
    get:
      summary: Get User Profile
      operationId: get_user_profile_api_v1_users__user_id__get
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
            title: User Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
  /api/v1/@me/mfa/totp/enable:
    post:
      summary: Set Authenticator Mfa
      operationId: set_authenticator_mfa_api_v1__me_mfa_totp_enable_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeviceRegistrationData'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - APIKeyHeader: []
  /api/v1/@me/mfa/totp/disable:
    post:
      summary: Set Authenticator Mfa
      operationId: set_authenticator_mfa_api_v1__me_mfa_totp_disable_post
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
      security:
        - APIKeyHeader: []
  /api/v1/@me:
    get:
      summary: Get Self Profile
      operationId: get_self_profile_api_v1__me_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
      security:
        - APIKeyHeader: []
  /api/v1/auth:
    post:
      summary: Authenticate
      operationId: authenticate_api_v1_auth_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AuthenticationData'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
  /api/v1/signup:
    post:
      summary: Signup
      operationId: signup_api_v1_signup_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AuthenticationData'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
  /:
    get:
      summary: Root
      operationId: root__get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
components:
  schemas:
    AuthenticationData:
      properties:
        username:
          type: string
          title: Username
        password:
          type: string
          title: Password
        code:
          type: string
          title: Code
        backup_code:
          type: string
          title: Backup Code
      type: object
      required:
        - username
        - password
      title: AuthenticationData
    DeviceRegistrationData:
      properties:
        password:
          type: string
          title: Password
        code:
          type: string
          title: Code
        secret:
          type: string
          title: Secret
      type: object
      required:
        - password
        - code
        - secret
      title: DeviceRegistrationData
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    APIKeyHeader:
      type: apiKey
      in: header
      name: X-Auth-Token

```

## Deployment
To deploy the project, run the following docker-compose file
```console
docker-compose -f docker-compose.yml up -d
```
