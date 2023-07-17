import axios from 'axios';
import {AppConfig} from '@/config.js'

/**
 * @typedef {object} MessageLogInfoDTO
 * @property {number} id
 * @property {number} study_id
 * @property {string} time
 * @property {Date} ts
 * @property {string} category
 * @property {string} status
 * @property {string} level
 * @property {string} provider
 * @property {string} description
 */

/**
 * @typedef {object} StudyInfoDTO
 * @property {number} id
 * @property {string} device
 * @property {string} status
 * @property {string} study
 * @property {Date} start_ts
 * @property {Date} end_ts
 */


/**
 * @class FeedbackService
 */
export class FeedbackService {
    /**
     * Fetches single message log info .
     * @param {number} messageId - The ID of the message.
     * @returns {Promise<MessageLogInfoDTO>} The message log information for the message.
     * @throws {Error} If the request fails.
     */
    static async getMessage(messageId) {
        try {
            const response = await axios.get(`${AppConfig.API_BASE_URL}/feedback/get_message?message_id=${messageId}`);
            return response.data;
        } catch (error) {
            throw new Error('Failed to get message with ID: '+messageId);
        }
    }

    /**
     * Fetches the message log info for a study.
     * @param {number} studyId - The ID of the study.
     * @returns {Promise<MessageLogInfoDTO[]>} The message log information for the study.
     * @throws {Error} If the request fails.
     */
    static async getMessageLog(studyId) {
        try {
            const response = await axios.get(`${AppConfig.API_BASE_URL}/feedback/get_message_log?study_id=${studyId}`);
            return response.data;
        } catch (error) {
            throw new Error('Failed to get message log for study ID: '+studyId);
        }
    }

    /**
     * Fetches the study header info for a study.
     * @param {number} studyId - The ID of the study.
     * @returns {Promise<StudyInfoDTO>} The study header information.
     * @throws {Error} If the request fails.
     */
    static async getStudyHeader(studyId) {
        try {
            const response = await axios.get(`${AppConfig.API_BASE_URL}/feedback/get_study_header?study_id=${studyId}`);
            return response.data;
        } catch (error) {
            throw new Error('Failed to get study header, ID: '+studyId);
        }
    }

    /**
     * Set the visibility of the message log for a given study ID.
     * @param {number} studyId - The ID of the study.
     * @param {boolean} visible - The visibility value to set.
     * @param {string} level - The level to update or '*' for any.
     * @returns {Promise<any>} A Promise that resolves with the response data.
     * @throws {Error} If there is an error setting the message log visibility.
     */
    static async setMessageLogVisibility(studyId, visible, level) {
        try {
            const response = await axios.get(`${AppConfig.API_BASE_URL}/feedback/set_message_log_visibility`, {
                params: {
                    study_id: studyId,
                    visible: visible,
                    level: level
                }
            });
            return response.data;
        } catch (error) {
            throw new Error('Failed to set message log visibility');
        }
    }
}

