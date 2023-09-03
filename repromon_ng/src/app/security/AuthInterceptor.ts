import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import {SecurityManager} from "./SecurityManager";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(
    private securityManager: SecurityManager,
  ) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    // get access token from localStorage or config
    const token = this.securityManager.getToken()

    // apply OAuth2+JWT Bearer token to the Authorization header.
    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`,
        },
      });
    }
    return next.handle(request);
  }
}
