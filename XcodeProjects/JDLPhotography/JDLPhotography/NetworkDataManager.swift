//
//  NetworkDataManager.swift
//  JDLPhotography
//
//  Created by Jonathan Long on 6/2/117.
//  Copyright © 2017 Jonathan Long. All rights reserved.
//

import UIKit
enum HTTPMethodType {
	case post
	case put
	case delete
	case get
}

//protocol NetworkDataManagerDelegate {
//	func networkDataManager(_ networkDataManager : NetworkDataManager, didReceive data: Data, response: URLResponse)
//	func networkDataManager(_ networkDataManager : NetworkDataManager, didReceive error: Error)
//}

typealias NetworkDataManagerCompletion = (Data, URLResponse) -> Void

class NetworkDataManager: NSObject, URLSessionDataDelegate {
	//MARK: Private Properties
	private let URLDelegateQ = OperationQueue()
	
	private var session : URLSession?
	
	private let baseURL : URL
	
	//MARK: Public Properties
//	var delegate : NetworkDataManagerDelegate?
	
//	init(url : URL, delegate : NetworkDataManagerDelegate?) {
//		baseURL = url
//		self.delegate = delegate
//		super.init()
//		session = URLSession(configuration: URLSessionConfiguration.default, delegate: self, delegateQueue: URLDelegateQ)
//	}
	
	init(url : URL) {
		baseURL = url
		super.init()
		session = URLSession(configuration: URLSessionConfiguration.default, delegate: self, delegateQueue: URLDelegateQ)
	}
	
	//MARK: Public
	func performRequest(_ method : HTTPMethodType, endpoint : String, completion: @escaping NetworkDataManagerCompletion) {
		let requestURL = baseURL.appendingPathComponent(endpoint)
		print("performing requst \(requestURL)")
		let request = NSMutableURLRequest(url: requestURL)
		switch method {
		case .post:
			request.httpMethod = "POST"
		case .delete:
			request.httpMethod = "DELETE"
		case .get:
			request.httpMethod = "GET"
		case .put:
			request.httpMethod = "PUT"
		}
		performRequest(request as URLRequest, completion: completion)
	}
	
	func performRequest(_ method : HTTPMethodType, url : URL, completion: @escaping NetworkDataManagerCompletion) {
		let request = NSMutableURLRequest(url: url)
		switch method {
		case .post:
			request.httpMethod = "POST"
		case .delete:
			request.httpMethod = "DELETE"
		case .get:
			request.httpMethod = "GET"
		case .put:
			request.httpMethod = "PUT"
		}
		performRequest(request as URLRequest, completion: completion)
	}
	
	//MARK: Private
	private func performRequest(_ request: URLRequest, completion: @escaping NetworkDataManagerCompletion) {
		if let dataTask = session?.dataTask(with: request, completionHandler: { (sessionData, sessionResponse, error) in
			
			if let err = error {
				print("There was an error with \(request) - \(err)")
			}
			
			if let data = sessionData, let response = sessionResponse {
				completion(data, response)
			}
		}) {
			dataTask.resume()
		}
		
	}
}
