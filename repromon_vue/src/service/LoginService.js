import axios from 'axios';
import {AppConfig} from '@/config.js'


/**
 * @typedef {object} LoginInfoDTO
 * @property {boolean} is_logged_in
 * @property {string} username
 * @property {string} first_name
 * @property {string} last_name
 */

/**
 * @class LoginService
 */
export class LoginService {
    /**
     * Fetches the current user's information.
     * @returns {Promise<LoginInfoDTO>} The current user's information.
     * @throws {Error} If the request fails.
     */
    static async getCurrentUser() {
        try {
            const response = await axios.get(`${AppConfig.API_BASE_URL}/login/get_current_user`);
            return response.data;
        } catch (error) {
            console.log("error="+error)
            throw new Error('Failed to get current user info');
        }
    }
}
